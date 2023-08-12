from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select

app = Flask(__name__)

# 创建数据库引擎
# 这里假设你的MySQL服务器在localhost，数据库名是mydatabase，用户名是myuser，密码是mypassword
# 根据你的实际情况修改这个URL
engine = create_engine('mysql+mysqlconnector://root:zhjl951753@remotehost:3307/ag')

# 反射数据库元数据
metadata = MetaData()
metadata.reflect(bind=engine)

# 获取对应的表
# 这里假设你的表名是`machines`
machines = Table('ag_machines', metadata, autoload_with=engine)


@app.route('/validate', methods=['POST'])
def validate():
    machine_code = request.form.get('machine_code')

    if not machine_code:
        return jsonify({"error": "机器码未提供"}), 400

    # 查询数据库
    with engine.connect() as connection:
        query = select(machines).where(machines.c.machine_code == machine_code)
        result = connection.execute(query)
        machine = result.fetchone()

        # 如果找到了对应的机器码，那么返回权限字段
        if machine is not None:
            return jsonify({"access_granted": machine.access_granted})
        # 如果没有找到对应的机器码，那么添加新的记录，并设置access_granted为False
        print("没有找到对应的机器码，添加新的记录")
        new_machine = machines.insert().values(machine_code=machine_code, access_granted=0)
        connection.execute(new_machine)
        connection.commit()
    # 如果没有找到对应的机器码，那么不允许运行程序
    return jsonify({"access_granted": 0})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8123)
