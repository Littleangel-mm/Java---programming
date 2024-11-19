import os
import requests

def download(ui):
    path = os.getcwd()
    url = ui.LineEdit.text()
    req = requests.get(url, verify=False ,stream=True)
    max = int(req.headers['content-length'])
    ui.jdt.setMaximum(max)
    vale = 0
    with open(path + "/" + url.split("/")[-1], "wb") as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                vale = vale + len(chunk)
                print(vale)
                ui.jdt.setValue(vale)



    # ui.jdt.setMaximum(100)
    # ui.max.setText("100")
    # ui.jdt.setMinimum(0)
    # for i in range(0, 101):
    #     ui.jdt.setValue(i)
    #     ui.small.setText(str(i))
    #     time.sleep(0.1)
