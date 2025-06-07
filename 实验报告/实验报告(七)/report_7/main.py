import plantuml
from pathlib import Path

# 定义PlantUML服务器URL（如果需要本地服务器，请修改此URL）
PLANTUML_SERVER = "http://www.plantuml.com/plantuml/svg/"

def generate_pos_system_state_diagram():
    """生成NextGen POS系统状态图"""
    # POS系统状态图的PlantUML代码
    plantuml_code = """
@startuml
hide empty description

[*] --> 商品扫描: 顾客到达

state 商品扫描 {
    [*] --> 扫描商品: 开始操作
    扫描商品 --> 扫描商品: 扫码/输入商品
    扫描商品 --> 累计金额: 商品录入
    累计金额 --> 扫描商品: 继续录入
    累计金额 --> 支付处理: 商品录入完成
}

state 支付处理 {
    [*] --> 验证支付信息: 开始支付
    验证支付信息 --> 支付成功: 信息有效
    验证支付信息 --> 支付失败: 信息无效
    支付失败 --> 异常处理: 触发异常
    支付成功 --> 库存更新: 支付完成
    验证支付信息 --> 离线模式: 网络中断
}

state 库存更新 {
    [*] --> 扣减库存: 处理中
    扣减库存 --> 更新成功: 库存充足
    扣减库存 --> 更新失败: 库存不足
    更新失败 --> 异常处理: 触发异常
    更新成功 --> 小票生成: 库存更新完成
    扣减库存 --> 离线模式: 网络中断
}

state 小票生成 {
    [*] --> 生成电子小票: 处理中
    生成电子小票 --> 打印纸质小票: 电子小票完成
    打印纸质小票 --> 交易完成: 小票打印成功
    生成电子小票 --> 异常处理: 打印失败
    打印纸质小票 --> 异常处理: 打印失败
    生成电子小票 --> 离线模式: 网络中断
}

state 异常处理 {
    [*] --> 记录错误: 错误捕获
    记录错误 --> 重试交易: 可恢复错误
    记录错误 --> 取消交易: 不可恢复错误
    重试交易 --> 支付处理: 重试支付
    重试交易 --> 库存更新: 重试库存更新
    重试交易 --> 小票生成: 重试打印小票
    取消交易 --> 商品扫描: 重新开始
}

state 离线模式 {
    [*] --> 缓存交易数据: 网络中断
    缓存交易数据 --> 继续现金支付: 允许操作
    继续现金支付 --> 离线完成: 现金支付成功
    离线完成 --> 小票生成: 生成离线小票
    缓存交易数据 --> 等待网络恢复: 网络不可用
    等待网络恢复 --> 同步云端: 网络恢复
    同步云端 --> [*]: 同步完成
}

交易完成 --> [*]: 顾客离开
@enduml
    """

    # 创建PlantUML对象
    puml = plantuml.PlantUML(url=PLANTUML_SERVER)
    
    # 生成SVG内容
    svg_content = puml.processes(plantuml_code)
    
    if svg_content:
        # 保存SVG文件
        output_file = Path("pos_system_state_diagram.svg")
        with open(output_file, 'wb') as f:
            f.write(svg_content)
        print(f"状态图已成功生成并保存到: {output_file}")
        return output_file
    else:
        print("生成状态图时出错")
        return None

if __name__ == "__main__":
    # 确保已安装plantuml库: pip install plantuml
    # 注意: 需要网络连接才能访问PlantUML服务器
    generate_pos_system_state_diagram()    