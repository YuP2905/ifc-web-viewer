<template>
<el-container>
    <el-header class="viewerSettingContainer">
            <el-upload
            :action="`${uploadUrl}/uploads`"
            ref="fileUpload"
            class="upload-demo"
            :accept="'.ifc'"
            show-file-list="true"
            :limit="1"
            :before-upload="beforeFileUpload"
            :on-success="handleFileUploadSuccess"
            :on-remove="handleFileRemove"
            :auto-upload="true">
                <el-button type="primary">Upload</el-button>
                <template #tip>
                    <div class="el-upload__tip">
                        Ifc file with a size less than 50M.
                    </div>
                </template>
            </el-upload>
            <el-switch
                v-model="isDisplayGrid"
                size="large"
                active-text="Grid"
                class="switch"
            />
            <el-switch
                v-model="isDisplayBackground"
                size="large"
                active-text="Background"
                class="switch"
            />
            <el-switch
                v-model="isHighlightElements"
                size="large"
                active-text="Highlight Selection"
                class="switch"
            />
            <el-button type="primary" :icon="OfficeBuilding" @click="fitViwerCamera" class="switch" >Fit</el-button>
            <el-select v-model="selectedCameraType" placeholder="Select Camera Type" style="width: 200px; margin-left: 20px;" @change="changeCameraType">
                <el-option 
                    v-for="item in selectData" 
                    :key="item.value" 
                    :label="item.label" 
                    :value="item.value" />
            </el-select>
    </el-header>
    <el-main >
        <el-row :gutter="20" :justify="'center'" style="height: 100%; min-height: 500px;" >
            <el-col :span="14" class="ifcViewer">
                <el-card shadow="always">
                <div id="ifcViwerContainer"></div>
                </el-card>
            </el-col>

            <el-col :span="10" class="IfcClassSetting">
                <el-select
                    v-model="selectedCategory"
                    placeholder="Select IFC Category"
                    style="width: 200px; margin-left: 20px;"
                    @change="ifcTypeFinder"
                >
                    <el-option
                        :key="'all'"
                        :label="'All'"
                        :value="null" 
                    />
                    <el-option
                        v-for="item in ifcTypeData"
                        :key="item.value"
                        :label="item.label"
                        :value="item.label"
                    />
                </el-select>

                <el-alert
                    v-if="randomElement"
                    type="success"
                    :closable="false"
                    show-icon
                    :description="getFormattedDescription(randomElement)"
                    style="font-size: 10px; padding: 10px; margin-top: 20px;"
                />

                <!-- 新增表格组件 -->
                <el-table
                    v-if="selectedElementsData.length > 0"
                    :data="selectedElementsData"
                    height="250"
                    size="small"
                    style="margin-top: 20px; font-size: 10px; width: 100%"
                    stripe
                >
                    <el-table-column
                        v-for="column in columns"
                        :prop="column.prop"
                        :label="column.label"
                        :key="column.prop"
                    />
                </el-table>

            </el-col>
    </el-row>
    </el-main>
</el-container>
</template>

<script>
import { ref, onMounted, watch} from "vue";
import { ElNotification } from "element-plus";
import { OfficeBuilding } from "@element-plus/icons-vue";
import "element-plus/es/components/notification/style/css";
import { Color, Mesh, MeshStandardMaterial } from "three";
import { Components, 
    Worlds, 
    SimpleScene, 
    OrthoPerspectiveCamera, 
    SimpleRenderer, 
    Grids, 
    Cullers, 
    IfcLoader, 
    Raycasters, 
    Classifier, 
    IfcFinder, 
    IfcBasicQuery,
    Hider} from "@thatopen/components";
// import { wasm } from "web-ifc";
// import { Highlighter, Outliner, PostproductionRenderer} from "@thatopen/components-front";

export default {
    name: "IfcViewer",
    setup() {
        const viewerComponents = ref(new Components());
        const viewerWorld = ref(null);
        const viewerGrids = ref(null);
        const viewerCaster = ref(null);
        const ifcFragments = ref(null);
        const isDisplayGrid = ref(true);
        const isDisplayBackground = ref(true);
        const isHighlightElements = ref(false);

        const fileUpload = ref(null);
        const uploadUrl = ref(null);
        const uploadedIfcUrl = ref("");
        const ifcModel = ref(null);
        const ifcFile = ref(null);
        const selectedCameraType = ref(1);
        const selectData = ref([
            {
                value: 1,
                label: "Perspective",
            },
            {
                value: 2,
                label: "Orthographic",
            }
        ]);
        const ifcTypeData = ref([]);
        const selectedCategory = ref(null);
        const selectedElementsData = ref([]);
        const randomElement = ref(null);
        const columns = ref([
            { prop: "ID", label: "ID" },
            { prop: "Type", label: "Type" },
            { prop: "Global_ID", label: "Global ID" },
            { prop: "Name", label: "Name" },
            { prop: "Description", label: "Description" },
            { prop: "ObjectType", label: "Object Type" },
            { prop: "ObjectPlacement", label: "Object Placement" },
            { prop: "Geometry_Representation", label: "Geometry Representation" },
            { prop: "Tag", label: "Tag" },
        ]);

        // 文件上传成功后的回调
        const handleFileUploadSuccess = async (response) => {
            if (response.fileUrl){
                uploadedIfcUrl.value = response.fileUrl;
                await loadFragments(uploadedIfcUrl.value);
                if (viewerWorld.value.scene && ifcModel.value){
                    viewerWorld.value.scene.three.add(ifcModel.value);
                    typeClassification();
                    if (isHighlightElements.value) {
                        selectElements();
                    }
                    ElNotification({
                        title: "Success",
                        message: "File uploaded successfully",
                        type: "success",
                    });
                }
            } else {
                ElNotification({
                    title: "Error",
                    message: "File upload failed",
                    type: "error",
                });
            }
        };

        // 取消文件的处理
        const handleFileRemove = async () => {
            if (viewerWorld.value.scene && ifcModel.value) {
                viewerWorld.value.scene.three.remove(ifcModel.value);
                ifcModel.value = null;
                window.onmousemove = null; // 移除鼠标移动的监听器
                ifcTypeData.value = [];
                selectedCategory.value = null; // 重置选择器的选项
                randomElement.value = null;
                selectedElementsData.value = [];
                ElNotification({
                    title: "Info",
                    message: "File removed successfully",
                    type: "info",
                });
            }
        };

        // 上传之前的文件验证逻辑
        const beforeFileUpload = (file) => {
            const isIFC = file.name.endsWith(".ifc");
            const isLt50M = file.size / 1024 / 1024 < 50;

            if (!isIFC) {
                ElNotification({
                title: "Warning",
                message: "Please upload an IFC file.",
                type: "Warning",
                });
                return false; // 阻止上传
            }
            if (!isLt50M) {
                ElNotification({
                title: "Warning",
                message: "File size exceeds the 50MB limit.",
                type: "Warning",
                });
                return false; // 阻止上传
            }

            return true; // 通过验证，允许上传
        };

        // 初始化场景
        function basicScenario(ifcViwerContainer) {
            // 实例化组件对象
            // viewerComponents.value = new Components(); 

            // 从实例对象(viewerComponents)中获取Worlds组件来管理world
            // 创建场景类型, 摄像机, 渲染器
            const viewWorld = viewerComponents.value.get(Worlds).create(
                SimpleScene,
                OrthoPerspectiveCamera,
                SimpleRenderer
                // PostproductionRenderer
            );

            // 设置场景, 相机和世界渲染器, 并调用init方法来启动渲染过程
            viewWorld.scene = new SimpleScene(viewerComponents.value);
            viewWorld.scene.setup(); // 添加灯光
            viewWorld.scene.three.background = null; // 背景透明

            // viewWorld.renderer = new PostproductionRenderer(viewerComponents.value, ifcViwerContainer);
            viewWorld.renderer = new SimpleRenderer(viewerComponents.value, ifcViwerContainer);
            viewWorld.camera = new OrthoPerspectiveCamera(viewerComponents.value);
            viewerComponents.value.init();

            //网格
            viewerGrids.value = viewerComponents.value.get(Grids).create(viewWorld);
            viewerGrids.value.config.visible = isDisplayGrid.value;
            viewerGrids.value.config.primarySize = 30; // 网格尺寸
            viewerGrids.value.config.secondarySize = 30;


            // 剔除器(隐藏场景中某些渲染对象. 提高性能)
            const viewerCuller = viewerComponents.value.get(Cullers).create(viewWorld);
            viewerCuller.config.threshold = 800; // 数字越大可见对象越少
            // 剔除器更新
            viewerCuller.needsUpdate = false;
            viewWorld.camera.controls.addEventListener("controlend", () => {
                viewerCuller.needsUpdate = true;
            });

            // 使用 Orthographic 相机时，如果相机缩小了很多，网格就会淡出。
            viewWorld.camera.projection.onChanged.add(() => {
                const projection = viewWorld.camera.projection.current;
                viewerGrids.value.fade = projection === "Perspective";
            });

            // 实例化raycaster
            viewerCaster.value = viewerComponents.value.get(Raycasters).get(viewWorld);
            viewerWorld.value = viewWorld;
        }

        async function loadFragments(fileUrl) {
            // const tiler = viewerComponents.value.get(IfcGeometryTiler);

            // tiler.settings.wasm = wasm;
            // tiler.settings.minGeometrySize = 20;
            // tiler.settings.minAssetsSize = 1000;

            ifcFragments.value = viewerComponents.value.get(IfcLoader);
            await ifcFragments.value.setup();

            ifcFragments.value.settings.webIfc.COORDINATE_TO_ORIGIN = true; // 移动至原点

            if (fileUrl) {
                const ifcFileResponse  = await fetch(fileUrl); // 获取文件的 Response 
                if (!ifcFileResponse.ok) {
                    ElNotification({
                        title: "Error",
                        message: `HTTP error! status: ${response.status}`,
                        type: "error",
                    });
                    throw new Error(`HTTP error! status: ${response.status}`);
                } else {
                    const ifcBufferData = await ifcFileResponse.arrayBuffer();
                    ifcFile.value = new File([ifcBufferData], "IFC_File")
                    const ifcArray = new Uint8Array(ifcBufferData);
                    ifcModel.value = await ifcFragments.value.load(ifcArray); // 没有await, 会返回promise
                }
            }
            
        }

        // 切换相机类型
        const changeCameraType = (cameraType) => {
            if (viewerWorld.value) {
                if (cameraType === 1){
                    viewerWorld.value.camera.projection.set(selectData.value[0].label);
                } else if (cameraType === 2){
                    // console.log(viewerWorld.value.camera.projection);
                    viewerWorld.value.camera.projection.set(selectData.value[1].label);

                }
            }
        }

        // 聚焦相机
        const fitViwerCamera = () => {
            if(viewerWorld.value && ifcModel.value){
                viewerWorld.value.camera.fit([ifcModel.value]);
            }

        }

        // 拾取模型
        const selectElements = () => {
            if (ifcModel.value) {
                let previousSelection = null;
                let previousMaterial = null;

                window.onmousemove = () => {
                    const viewerResult = viewerCaster.value.castRay([ifcModel.value]);
                    if (previousSelection) {
                        previousSelection.material = previousMaterial; // 恢复为原来的颜色
                    }
                    if (!viewerResult || !(viewerResult.object instanceof Mesh)) {
                        return;
                    }
                    previousSelection = viewerResult.object;
                    previousMaterial = previousSelection.material;
                    viewerResult.object.material = new MeshStandardMaterial({ color: "#BCF124" });
                    // previousSelection = viewerResult.object;
                };
            }
        }

        //IFC分类器
        const typeClassification = () => {
            if (ifcModel.value) {
                const ifcClassiFier = viewerComponents.value.get(Classifier);
                ifcClassiFier.byEntity(ifcModel.value);
                
                const classificationData = [];
                Object.entries(ifcClassiFier.list.entities).forEach(([key, value], index) => {
                    if (value) {
                        classificationData.push({
                            label: key,   // IFC 类别名称，IFCWALL, IFCWINDOW 等
                            value: index  // 使用索引作为 value
                        });
                    }
                });
                ifcTypeData.value = classificationData;
            }
        }

        // 后端请求
        const sendBackendRequest = (category) => {
            fetch(`${uploadUrl.value}/find-ifc-elements`, 
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ category: category }),
            }).then(response => response.json())
            .then(data => {
                // 更新前端数据
                selectedElementsData.value = data.elements;  // 将所有符合条件的元素更新到表格中
                if (data.elements.length > 0) {
                    randomElement.value = data.elements[Math.floor(Math.random() * data.elements.length)];

                } else {
                    randomElement.value = null;
                }
            }).catch(error => {
                console.error("Error fetching elements from backend:", error);
                ElNotification({
                    title: "Erro",
                    message: `Error executing the query: ${error}`,
                    type: "error",
                });
                });
        }

        const getFormattedDescription = (element) => {
            const descriptionList = [];

            if (element.ID) descriptionList.push(element.ID);
            if (element.Type) descriptionList.push(element.Type);
            if (element.Global_ID) descriptionList.push(element.Global_ID);
            if (element.Name) descriptionList.push(element.Name);
            if (element.Description) descriptionList.push(element.Description);
            if (element.ObjectType) descriptionList.push(element.ObjectType);
            if (element.ObjectPlacement) descriptionList.push(element.ObjectPlacement);
            if (element.Geometry_Representation) descriptionList.push(element.Geometry_Representation);
            if (element.Tag) descriptionList.push(element.Tag);

            return descriptionList.join(', ');
        };

        // 函数: 排序 randomElement 中的键
        const elementDisplayOrder = (element) => {
            const orderedKeys = [
                "ID",
                "Type",
                "Global_ID",
                "Name",
                "Description",
                "ObjectType",
                "ObjectPlacement",
                "Geometry_Representation",
                "Tag"
            ];

            const orderedElement = {};
            orderedKeys.forEach((key) => {
                if (element[key] !== undefined && element[key] !== null) {
                    orderedElement[key] = element[key];
                }
            });
            return orderedElement;
        };

        // IFC查找器
        const ifcTypeFinder = (category) => {
            const ifcHider = viewerComponents.value.get(Hider);
            if (!category) {
                ifcHider.set(true); // 显示所有构件

                // 清空随机说明和表格数据
                randomElement.value = null;
                selectedElementsData.value = [];
                return;
            }

            if (ifcModel.value) {
                sendBackendRequest(category); // 请求前端
                const ifcFinder = viewerComponents.value.get(IfcFinder); // 获取Finder实例
                const queryGroup = ifcFinder.create(); // 创建查询组

                // 创建基本查询
                const basicQuery = new IfcBasicQuery(viewerComponents.value, {
                    name: "category",
                    inclusive: false,
                    rules: [],
                });

                // 设置类别规则，选择的类别
                const categoryRule = {
                    type: "category", // 按照类别查询
                    value: new RegExp(category, 'i'), // 使用正则表达式匹配类别
                };
                basicQuery.rules.push(categoryRule); // 将规则添加到查询中
                queryGroup.add(basicQuery); // 添加查询到查询组

                queryGroup.update(ifcModel.value.uuid, ifcFile.value).then(() => {
                    const ifcElements = queryGroup.items; // 获取符合条件的构件

                    if(Object.keys(ifcElements).length > 0){

                        // const ifcHider = viewerComponents.value.get(Hider); // 使用 Hider 控制可见性
                        ifcHider.set(false); // 首先隐藏所有
                        ifcHider.set(true, ifcElements); // 显示符合条件的构件

                    } else {
                        ElNotification({
                            title: "Warning",
                            message: "No elements found for the selected category.",
                            type: "warning",
                        });
                    }
                }).catch((error) => {
                    ElNotification({
                        title: "Erro",
                        message: `Error executing the query: ${error}`,
                        type: "error",
                    });
                })
            }

        }

        // 监视渲染
        watch(isHighlightElements, (newValue) => {
            if (newValue && ifcModel.value) {
                selectElements();
            } else {
                window.onmousemove = null; // 移除事件监听器
            }
        });


        // 监视显示网格按钮
        watch(isDisplayGrid, (newValue) => {
            if (viewerWorld.value.scene) {
                viewerGrids.value.config.visible = newValue; // 动态更新网格可见性
            }
        });

        // 监视显示背景颜色
        watch(isDisplayBackground, (newValue) => {
            if (viewerWorld.value && viewerWorld.value.scene) {
                viewerWorld.value.scene.three.background = newValue ? null : new Color(0x000000);
            }
        });

        onMounted(async function () {

            // 获取IP地址
            const response = await fetch (
                "http://localhost:5000/server-ip",
                {
                    method: "GET",
                }
            )
            if (!response.ok) {
                ElNotification({
                        title: "Error",
                        message: `HTTP error! status: ${response.status}`,
                        type: "error",
                });
                throw new Error(`HTTP error! status: ${response.status}`);
            } else {
                const getedData = await response.json();
                uploadUrl.value = `http://${getedData.serverIp}:5000`;
                
            }

            // 获取IfcViwer容器
            const ifcViwerContainer = document.getElementById("ifcViwerContainer");
            basicScenario(ifcViwerContainer);
            // if (ifcModel.value) {
            //     typeClassification();
            // }
        });

        return {
            OfficeBuilding,
            uploadUrl,
            fileUpload,
            isDisplayGrid,
            isDisplayBackground,
            beforeFileUpload,
            handleFileUploadSuccess,
            handleFileRemove,
            selectData,
            selectedCameraType,
            changeCameraType,
            fitViwerCamera,
            isHighlightElements,
            ifcTypeData,
            selectedCategory,
            ifcTypeFinder,
            randomElement,
            getFormattedDescription,
            selectedElementsData,
            columns,
        };
    },
};
</script>
    
<style scoped>
.viewerSettingContainer {
    /* 设置容器宽度为100%，高度为80px */
    width: 100%;
    height: 80px;

    /* 使用Flexbox布局，gap设置组件之间的间距为15px，排列方式为水平方向 */
    display: flex;
    gap: 15px;
    flex-direction: row;

    /* 设置组件之间的空白区域为等距排列，垂直方向居中对齐 */
    justify-content: space-around;
    align-items: center;

    /* 设置背景颜色为浅灰色，圆角为8px */
    /* background-color: #f5f5f5; */
    padding: 10px 20px;
    border-radius: 8px;

    /* 添加阴影效果，提供层次感 */
    /* box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); */
}

.ifcViwer {
    /* 设置宽度和高度为父容器的100% */
    width: 100%;
    height: 100%;

    /* 使用Flexbox布局，内容水平垂直居中对齐 */
    display: flex;
    justify-content: center;
    align-items: center;

    /* 设置圆角为8px，并添加阴影效果 */
    border-radius: 8px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);

    /* 防止内容溢出 */
    overflow: hidden;
}

#ifcViwerContainer {
    /* 设置宽度为100%，高度为500px的容器 */
    width: 100%;
    height: 500px;

    /* 设置圆角和溢出处理 */
    border-radius: 8px;
    overflow: hidden;
}

#ifcViwerContainer canvas {
    /* 设置Canvas元素的宽高为100% */
    width: 100%;
    height: 100%;

    /* 去掉Canvas的外边距 */
    margin: 0px;
}

.switch {
    /* 设置switch控件的左外边距为10px */
    margin-left: 10px;
}

.IfcClassSetting {
    /* 设置宽度和高度为父容器的100%，并增加内边距 */
    width: 100%;
    height: 100%;
    padding: 10px;

    /* 设置背景颜色为淡灰色，圆角为8px */
    /* background-color: #fafafa; */
    border-radius: 8px;

    /* 添加轻微的阴影效果，增强视觉层次 */
    /* box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05); */
}

.el-upload__tip {
    /* 设置提示文字颜色为浅灰色，字体大小为12px */
    color: #606266;
    font-size: 12px;

    /* 设置提示文字上方的外边距为5px */
    margin-top: 5px;
}


</style>
    