from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os, socket
import ifcopenshell


# 创建实例
app = Flask(__name__) 

"""
解决跨域问题
"/uploads/*"   允许访问/uploads路径下的任何文件
"origins": "*"  允许任何来源访问

"""
# 解决跨域问题
CORS(app, resources={
    "/uploads/*": {"origins": "*"}, 
    "/server-ip": {"origins": "*"},
    "/find-ifc-elements": {"origins": "*"}
})


# 上传文件夹路径/路由路径
UPLOAD_FOLDER = "/uploads"
ifc_file_path = None
ifc_model = None

@app.route('/', methods=["GET"])
def home():
    return "Flask File Upload Server is Running!", 200

# 返回当前服务器的 IP 地址
@app.route("/server-ip", methods=["GET"])
def get_server_ip():
    hostname = socket.gethostname()
    server_ip = socket.gethostbyname(hostname)
    return jsonify({"serverIp": server_ip}), 200

# 上传文件到uploads路由
@app.route("/uploads", methods=["POST"]) # 只允许Post请求
def upload_file():
    global ifc_file_path, ifc_model

    # 检测是否上传了文件
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files["file"]

    # 清空上传目录
    for file_name in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    # 保存新上传的文件
    ifc_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(ifc_file_path)

    # 读取 IFC 模型
    ifc_model = ifcopenshell.open(ifc_file_path)

    # 返回文件的 URL 以供前端使用
    file_url = f"{request.host_url}uploads/{file.filename}"
    return jsonify({"fileUrl": file_url}), 200

@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 根据类别查找 IFC 元素
@app.route("/find-ifc-elements", methods=['POST'])
def find_ifc_elements():
    global ifc_model

    if ifc_model is None:
        return jsonify({"error": "No IFC model loaded"}), 400

    data = request.get_json()
    category = data.get("category")

    if not category:
        return jsonify({"error": "No category specified"}), 400

    # 查找所有属于指定类别的元素
    elements = []
    for element in ifc_model.by_type(category):
        elements.append({
            "ID": f"#{element.id()}",
            "Type": element.is_a(),
            "Global_ID": element.GlobalId if hasattr(element, "GlobalId") else None,
            "Name": element.Name if hasattr(element, "Name") else None,
            "Description": element.Description if hasattr(element, "Description") else None,
            "ObjectType": element.ObjectType if hasattr(element, "ObjectType") else None,
            "ObjectPlacement": f"#{element.ObjectPlacement.id()}" if hasattr(element, "ObjectPlacement") else None,
            "Geometry_Representation": str(element.Representation) if hasattr(element, "Representation") else None,
            "Tag": element.Tag if hasattr(element, "Tag") else None,
        })

    return jsonify({"elements": elements})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
