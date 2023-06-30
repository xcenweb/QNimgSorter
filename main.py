import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.simpledialog

import threading
import sys
import tool
import time
import imghdr
import glob
import os
import shutil
import wget
import ssl
from multiprocessing import freeze_support

freeze_support()

__LOCAL_DIR__ = os.path.dirname(os.path.realpath(sys.argv[0]))

class ConsoleUi(tkinter.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        # 可滚动文本框
        self.text = tkinter.scrolledtext.ScrolledText(self)
        self.text.pack(side='left')
        
        # 右侧按钮组
        self.btnframe = tkinter.Frame(self,width=80,height=400,relief='groove',bd=1)
        self.btnframe.pack(side='right')

        self.btn_0 = tkinter.Button(self.btnframe, text="1.下载", command=self.btn_event_download)
        self.btn_0.pack(pady=10)

        self.btn_1 = tkinter.Button(self.btnframe, text="2.分类", command=self.btn_event_sort)
        self.btn_1.pack(pady=10)

        self.btn_2 = tkinter.Button(self.btnframe, text="3.插入名字", command=self.btn_event_insert)
        self.btn_2.pack(pady=10)

        self.btn_3 = tkinter.Button(self.btnframe, text="4.打包", command=self.btn_event_pack)
        self.btn_3.pack(pady=10)

        # 版权
        self.textprint('开发者：一只咕鸽(xcenweb@qq.com)\n开发者微信：ITxcen1618000')

    # 图片分类事件
    def btn_event_sort(self):
        t = threading.Thread(target=self.func_sort,args=())
        t.start()
    def func_sort(self):

        # ====================== 基本配置 =========================

        self.textprint("\n\n开始分类图片......")
        
        init_source_path = __LOCAL_DIR__ + '\\images\\'  # 存储原始待分类图片文件夹
        init_sorted_path = __LOCAL_DIR__ + '\\sorted\\'  # 存储分类后图片的文件夹
        
        future_rgbs_a = tool.read_image_RGB(__LOCAL_DIR__ + '\\标准个人主页.jpg', max_colors=5)  # 标准的第一组RGB值（个人主页）
        future_rgbs_b = tool.read_image_RGB(__LOCAL_DIR__ + '\\标准完成截图.jpg', max_colors=5)  # 标准的第二组RGB值（看完后的截图）

        self.textprint("\n\n开始处理图片......")

        # =========================================================

        for file_abs in glob.glob(init_source_path + '*'):
            if imghdr.what(file_abs) in {'jpg', 'png', 'jpeg'}:
                image_name = file_abs.replace(init_source_path, '')  # 图片名称
                image_rgbs = tool.read_image_RGB(image = file_abs, max_colors = 5)  # 图片RGB组

                self.textprint('-' * 10 + '\n正在读取并对比图片：' + image_name + '.' * 6)

                group_a = tool.rgb_similarity(future_rgbs_a, image_rgbs)  # 第一组 比对
                group_b = tool.rgb_similarity(future_rgbs_b, image_rgbs)  # 第二组 比对

                # 实时回调
                # self.textprint('=> A:' + str(group_a) + ' B:' + str(group_b))

                # 开始比对
                if group_a > group_b:
                    self.textprint('对比结果：个人主页\n移动结果：' + str(tool.move_file(file_abs, init_sorted_path + '青年大学习2')))
                elif group_a < group_b:
                    self.textprint('对比结果：看完后截图\n移动结果：' + str(tool.move_file(file_abs, init_sorted_path + '青年大学习1')))
                else:
                    continue
            time.sleep(0.2)
        tkinter.messagebox.showinfo('提示', '分类完成！请检查分类结果然后再进行下步操作！')
        os.startfile(init_sorted_path)

    # 下载zip文件并解压，针对接龙管家
    def btn_event_download(self):
        link = tkinter.simpledialog.askstring(title="下载链接", prompt="请输入已收集截图的压缩包下载链接", initialvalue="http://")
        ssl._create_default_https_context = ssl._create_unverified_context  # 取消ssl全局验证
        
        self.textprint('开始下载目标文件...')
        file = wget.download(link, out=__LOCAL_DIR__ + '\\data.zip')
        
        self.textprint('已下载：[' + file + '] 开始解压...')
        shutil.unpack_archive(file, __LOCAL_DIR__ + '\\images')
        os.remove(file)
        self.textprint('done.')
        tkinter.messagebox.showinfo('提示', '目标压缩包下载解压成功，可以进行下一步操作！')

    # 为每张图片强行插入名字
    def btn_event_insert(self):
        t = threading.Thread(target=self.func_insert,args=())
        t.start()
    def func_insert(self):
        if tkinter.messagebox.askokcancel('提示', '请确认分类无误，点击确认继续该操作！'):
            tkinter.messagebox.showwarning('警告', '此功能暂时不可用！')
        else:
            self.textprint('\n操作取消：强行插入名字')

    # 打包图片
    def btn_event_pack(self):
        t = threading.Thread(target=self.func_pack,args=())
        t.start()
    def func_pack(self):
        if tkinter.messagebox.askokcancel('提示', '请确认分类无误，点击确认继续该操作！'):
            shutil.make_archive(os.path.join(os.path.expanduser("~"), 'Desktop') + '\\青年大学习', 'zip', __LOCAL_DIR__ + '\\sorted\\')
            shutil.rmtree(__LOCAL_DIR__ + '\\sorted\\')
            tkinter.messagebox.showinfo('提示', '打包成功！打包后的文件在桌面！')
        else:
            self.textprint('\n操作取消:打包')
    
    # 在点击按钮时运行程序，并将结果输出到文本控件中
    def textprint(self, text):
        self.text.insert('end', text + "\n")
        self.text.see('end')

    

# 创建主窗口
root = tkinter.Tk()
root.title('青年大学习截图分类 V1.0 - powered by 徐涔峰')
root.iconbitmap('favicon.ico')
width = 700
height = 350
root.geometry('{}x{}+{}+{}'.format(width, height, int((root.winfo_screenwidth()-width)/2), int((root.winfo_screenheight()-height)/2)-80))
root.resizable(False, False)

# 启动应用程序
app = ConsoleUi(master=root)
app.mainloop()