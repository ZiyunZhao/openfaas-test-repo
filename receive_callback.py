from flask import Flask
from flask import request
import time
import numpy as np
app = Flask(__name__)
import requests

end = []

@app.route('/', methods=['GET', 'POST'])
def receive():
    global end
    end.append(time.time())
    return request.data

if __name__=='__main__':
    app.run()
    print("time span:",end[-1] - end[0])
    print("total received:", len(end))
    np.save("endtime", end)
