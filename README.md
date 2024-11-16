# Video
<video id="video" controls="" preload="none" poster="" src="./video/video.mp4"></video>


# Project Name: ifc-web-viewer

ifc-web-viewer is a full-stack project based on Vue.js and Flask. The front end is built with Vue.js, while the back end uses Flask to provide API services. This application allows users to upload, view, and interact with IFC files. It supports features such as grid display, background toggle, element highlighting, and camera control.

## Project Structure

```
my_project/
├── client/        # Frontend Vue project
└── backend/       # Backend Flask project
```

- `client/` directory contains the frontend code, built with Vue.js.
- `backend/` directory contains the backend code, implemented with Flask.

## Setup Environment

### Frontend (Vue.js)

1. Navigate to the `client` directory:

   ```sh
   cd client
   ```

2. Install dependencies:

   ```sh
   npm install
   ```

3. Start the development server:

   ```sh
   npm run serve
   ```

### Backend (Flask)

1. Activate the virtual environment:

   ```sh
   conda activate <your_environment_name>
   ```

2. Install dependencies:

   ```sh
   pip install -r backend/requirements.txt
   ```

3. Start the Flask server:

   ```sh
   cd backend
   python backendServe.py
   ```

## Project Startup

1. Run the following commands in the root directory to start both frontend and backend services:

   ```sh
   start cmd /k "cd client && npm run serve"
   cd backend
   conda activate <your_environment_name>
   python backendServe.py
   ```

2. The frontend and backend services will start in separate command line windows.

## Dependency Management

- Frontend dependencies are managed with `npm` and can be installed using `npm install`.
- Backend dependencies are recorded in the `requirements.txt` file and can be installed using `pip install -r requirements.txt`.

## Directory Description

- `client/`: Frontend code, based on Vue.js.
- `backend/`: Backend code, based on Flask, containing API implementation.

## Notes

- Make sure to activate the correct virtual environment before running the Flask backend.
- The frontend and backend services should run in separate terminal windows to allow simultaneous access.

## Acknowledgments

This project uses components developed by [engine_components](https://github.com/ThatOpen/engine_components), and libraries developed by [ifcopenshell](https://github.com/IfcOpenShell/IfcOpenShell). I would like to thank the developers for their contributions.

## Contribution

Feel free to submit a Pull Request or report issues. Your contributions are appreciated!

## Future Plans

1. **Other IFC-related analysis tools with data export support.**
2. **Potential machine learning features to enhance analysis capabilities.**

---

# 项目名称: ifc-web-viewer

ifc-web-viewer 是一个基于 Vue.js 和 Flask 的全栈项目。前端使用 Vue.js 构建，后端使用 Flask 提供 API 服务。该应用允许用户上传、查看和交互 IFC 文件，支持网格显示、背景切换、构件高亮和相机控制等功能。

## 项目结构

```
my_project/
├── client/        # 前端 Vue 项目
└── backend/       # 后端 Flask 项目
```

- `client/` 目录包含前端代码，使用 Vue.js 构建。
- `backend/` 目录包含后端代码，使用 Flask 实现。

## 环境搭建

### 前端 (Vue.js)

1. 进入 `client` 目录：

   ```sh
   cd client
   ```

2. 安装依赖：

   ```sh
   npm install
   ```

3. 启动开发服务器：

   ```sh
   npm run serve
   ```

### 后端 (Flask)

1. 激活虚拟环境：

   ```sh
   conda activate <your_environment_name>
   ```

2. 安装依赖：

   ```sh
   pip install -r backend/requirements.txt
   ```

3. 启动 Flask 服务器：

   ```sh
   cd backend
   python backendServe.py
   ```

## 项目启动

1. 在根目录下运行以下命令来启动前端和后端服务：

   ```sh
   start cmd /k "cd client && npm run serve"
   cd backend
   conda activate <your_environment_name>
   python backendServe.py
   ```

2. 前端和后端服务将分别在不同的命令行窗口中启动。

## 依赖管理

- 前端依赖使用 `npm` 管理，可以通过 `npm install` 安装。
- 后端依赖记录在 `requirements.txt` 文件中，可以通过 `pip install -r requirements.txt` 安装。

## 目录说明

- `client/`：前端代码，基于 Vue.js。
- `backend/`：后端代码，基于 Flask，包含 API 实现。

## 注意事项

- 确保在运行 Flask 后端之前激活正确的虚拟环境。
- 前端和后端服务应在不同的终端窗口中运行，以便同时访问。

## 鸣谢

本项目使用了 [engine_components](https://github.com/ThatOpen/engine_components) 开发的组件和 [ifcopenshell](https://github.com/IfcOpenShell/IfcOpenShell) 开发的库，感谢开发者们的贡献。

## 贡献

欢迎提交 Pull Request 或报告问题，感谢你的贡献！

## 未来规划

1. **其他 IFC 相关的基础分析工具，支持数据导出。**
2. **可能添加一些机器学习内容，用于增强分析功能。**

