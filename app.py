from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    total_amount = int(request.form['totalAmount'])
    number_of_people = int(request.form['numberOfPeople'])
    pay_more_percent = int(request.form['payMorePercent'])
    pay_more_amount = int(request.form['payMoreAmount'])
    zakkuri_flag = request.form.getlist('zakkuriFlag')

    # 多めにパーセンテージを払う人がいる場合
    if pay_more_percent > 0:
        if total_amount % number_of_people == 0:
            if pay_more_percent % number_of_people == 0:
                pay_more_percent_1 = pay_more_percent // number_of_people
                pay_more_percent_2 = pay_more_percent - pay_more_percent_1
                split_amount_1 = (total_amount / number_of_people) * (100+pay_more_percent_1) // 100 
                split_amount_2 = (total_amount / number_of_people) * (100-pay_more_percent_2) // 100 
        else:
            pay_more_percent_2 = pay_more_percent / 2
            pay_more_percent_1 = pay_more_percent - pay_more_percent_2
            split_amount_1 = total_amount / number_of_people  * (100+pay_more_percent_1) // 100 + 1 
            split_amount_2 = total_amount / number_of_people  * (100-pay_more_percent_2) // 100 + 1
    
    # 多めに金額を払う人がいる場合
    elif pay_more_amount > 0:
        if total_amount % number_of_people == 0:
            pay_more_amount_1 = pay_more_amount // number_of_people
            pay_more_amount_2 = pay_more_amount - pay_more_amount_1
            split_amount_1 = total_amount / number_of_people  + pay_more_amount_1
            split_amount_2 = total_amount / number_of_people  - pay_more_amount_2
        else:
            pay_more_amount_1 = pay_more_amount // number_of_people
            pay_more_amount_2 = pay_more_amount - pay_more_amount_1
            split_amount_1 = total_amount // number_of_people + 1 + pay_more_amount_1
            split_amount_2 = total_amount // number_of_people - pay_more_amount_2
    
    # 多めに払う人がいない場合    
    elif (pay_more_amount is None or pay_more_amount == 0) and (pay_more_percent is None or pay_more_percent == 0):
        # 合計金額/人数のあまりが0の場合
        if total_amount % number_of_people == 0:
            split_amount_1 = total_amount / number_of_people
            split_amount_2 = total_amount / number_of_people
        # 切り捨て+1円を割り勘の金額にする
        if total_amount % number_of_people != 0:
            split_amount_1 = total_amount // number_of_people + 1
            split_amount_2 = total_amount // number_of_people
            
    # ざっくり計算する場合
    if '10' in zakkuri_flag:
        split_amount_1 = round(split_amount_1+5,-1)
        split_amount_2 = round(split_amount_2+5,-1)
            
    # 合計金額の調整
    sabun = total_amount - split_amount_1 - split_amount_2
    if sabun == 0:
        pass
    else:
        for i in range (int((sabun+1) //number_of_people)):
            if sabun > 0 :
                split_amount_1 = split_amount_1 + 1                
                split_amount_2 = split_amount_2 + 1
                sabun = sabun - 2
            elif sabun == 1:
                split_amount_1 = split_amount_1 + 1                
                break
            elif sabun == -1:
                split_amount_1 = split_amount_1 + 1                
                break
            elif sabun < 0:
                split_amount_1 = split_amount_1 + 1                
                split_amount_2 = split_amount_2 + 1
                sabun = sabun - 2
            else:
                break
                
    # 割り勘の金額を返却
    return render_template('result.html', split_amount_1=math.floor(split_amount_1), split_amount_2=math.floor(split_amount_2))

if __name__ == '__main__':
    app.run(debug=True)
    
