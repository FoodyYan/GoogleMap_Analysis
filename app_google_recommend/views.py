from django.shortcuts import render
from django.http import  JsonResponse
import pandas as pd

# render渲染網頁
def chart_cate_topword(request):
    return render(request, 'app_google_recommend/home.html')

# read df
df_topkey = pd.read_csv('app_google_recommend/dataset/google_comment_frequency.csv', sep='|')
df_topkey2 = pd.read_csv('app_google_recommend/dataset/google_date.csv',sep='|')

# prepare data
data={}
date_data={}
for idx, row in df_topkey.iterrows():
    data[row['category']] = eval(row['top_keys'])


# df_ => 必吃店家資訊
df_info = pd.read_csv('app_google_recommend/dataset/google_info_preprocessed(1).csv', sep=',')
# prepare data
data_info = df_info.values.tolist()


for idx, row in df_topkey2.iterrows():
    date_data[row['time']] = eval(row['test'])
# We don't use it anymore, so delete it to save memory.
del df_topkey
del df_topkey2

# POST: csrf_exempt should be used
# 指定這一支程式忽略csrf驗證
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_get_cate_topword(request):
    if request.POST.get('type') == 'top':
        cate = request.POST.get('news_category')
    #cate = request.POST['news_category']  # this command also works.
        topk = request.POST.get('topk')
        topk = int(topk)
        print(cate, topk)    
        chart_data, wf_pairs = get_category_topword(cate, topk)
        response = {'chart_data': chart_data,
         'wf_pairs': wf_pairs,
        }

    elif request.POST.get('type') == 'date':
        date_cate = request.POST.get('date_')
        print(date_cate)
        chart_data2,wf_pairs2 = get_date(date_cate)
        response = {'chart_data2': chart_data2,
         'wf_pairs2': wf_pairs2,
        }

    print(response)
    return JsonResponse(response)

def get_date(date_cate):
    wf_pairs2 = date_data[date_cate][0:10]
    words = [w for w, f in wf_pairs2]
    freqs = [f for w, f in wf_pairs2]
    chart_data2 = {
        "category": date_cate,
        "labels": words,
        "values": freqs}
    return chart_data2,wf_pairs2


def get_category_topword(cate, topk=10):
    wf_pairs = data[cate][0:topk]
    words = [w for w, f in wf_pairs]
    freqs = [f for w, f in wf_pairs]
    chart_data = {
        "category": cate,
        "labels": words,
        "values": freqs}
    return chart_data, wf_pairs

@csrf_exempt
def api_get_cate_info(request):
    cate = request.POST.get('news_category')
    print(cate)
    info = []
    print(cate)
    print(data_info)
    for i in data_info:
        if i[0] == cate:
            info = i
            break
    info_data = {
        "info_data": info,
        "cate": cate}
    return JsonResponse(info_data)

print("app_top_keywords--類別熱門關鍵字載入成功!")
