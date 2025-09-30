import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from tqdm import tqdm
import os
from matplotlib.font_manager import FontProperties


def find_mp4_files(directory):
    path_list = []
    file_list = []

    # 遍历目录树
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp4'):
                full_path = os.path.join(root, file)
                path_list.append(full_path)
                file_list.append(file)

    return path_list, file_list


def create_video_color_timeline(video_path, file_name, output_path="color_timeline.png", dpi=100):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("无法打开视频文件")
        return None

    # 获取视频信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    # 收集每秒第一帧的平均颜色
    colors = []
    seconds = int(duration)

    # 使用tqdm显示进度条，按秒处理
    for second in tqdm(range(seconds), desc="处理视频秒", unit="秒"):
        # 计算这一秒的第一帧位置
        target_frame = int(second * fps)

        # 跳转到目标帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        ret, frame = cap.read()

        if ret:
            # 将BGR转换为RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 计算当前帧的平均颜色
            avg_color = np.mean(frame_rgb, axis=(0, 1)).astype(np.uint8)
            colors.append(avg_color)
        else:
            # 如果读取失败，使用黑色
            colors.append(np.array([0, 0, 0], dtype=np.uint8))

    # 释放视频资源
    cap.release()

    if not colors:
        print("未成功读取任何帧")
        return None

    # 创建图形，设置物理尺寸为20英寸×5英寸
    fig_width_inch = 20
    fig_height_inch = 5

    fig, ax = plt.subplots(figsize=(fig_width_inch, fig_height_inch), dpi=dpi)

    # 计算每个小矩形的宽度（在20英寸长度上平均分成n份）
    n = len(colors)
    segment_width_inch = fig_width_inch / n  # 每个小矩形的宽度（英寸）

    # 使用tqdm显示创建矩形的进度
    for i, color in enumerate(tqdm(colors, desc="生成颜色条", unit="矩形")):
        # 将RGB颜色值从0-255转换到0-1范围
        color_normalized = color / 255.0

        # 计算第i个小矩形的起始位置（英寸）
        start_x_inch = i * segment_width_inch

        # 创建第i个小矩形，填充第i秒第一帧的平均颜色
        rect = Rectangle((start_x_inch, 0), segment_width_inch, fig_height_inch,
                         facecolor=color_normalized,
                         edgecolor='none',  # 无边框
                         linewidth=0)
        ax.add_patch(rect)

    # 创建字体属性，使用本地字体文件
    font_path = r"D:\WorkPC\2_Code\HouseKnowledgeGraphSystem\font\微软雅黑.ttf"
    font_prop = FontProperties(fname=font_path)

    # 在画面正中添加文本
    ax.text(fig_width_inch / 2, fig_height_inch / 2, f'EP{file_name}',
            fontproperties=font_prop,  # 使用自定义字体
            fontsize=60,  # 设置字体大小
            color='white',  # 设置字体颜色为白色，在彩色背景上更清晰
            ha='center',  # 水平居中
            va='center',  # 垂直居中
            weight='bold',  # 粗体
            bbox=dict(boxstyle="round,pad=0.3", facecolor="black", alpha=0.7)  # 添加背景框
            )

    # 设置坐标轴范围
    ax.set_xlim(0, fig_width_inch)
    ax.set_ylim(0, fig_height_inch)

    # 隐藏坐标轴
    ax.set_axis_off()

    # 调整布局，确保整个画布都被使用
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # 保存图片，保持准确的物理尺寸
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', pad_inches=0)

    return colors


# 使用示例
def main():
    # 使用您的视频文件路径
    path_list, file_list = find_mp4_files(r"C:\Users\liang\Downloads\try")
    for i, path in enumerate(path_list):
        print(f"{i+1}/{len(path_list)} 正在处理：{file_list[i]} ")
        create_video_color_timeline(path, file_list[i], rf"{path[:-4]}_timeline.png")


if __name__ == "__main__":
    main()

