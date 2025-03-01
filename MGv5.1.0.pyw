import time
import customtkinter as ctk
import os
import re
import threading
import pyperclip
import pytubefix
import yt_dlp
from PIL import Image
import requests
from io import BytesIO
# إعداد الستايل
ctk.set_appearance_mode("dark")  # أو "dark" لو عايز الوضع الليلي
ctk.set_default_color_theme("blue")  # يمكنك تجربة "green" أو "dark-blue"


# إنشاء النافذة
root = ctk.CTk()
root.title("MG v:5.1.0")
root.geometry("900x650+300+50")
dc=ctk.CTkButton(root)
default_color = dc.cget("fg_color")  # لـ CustomTkinter
#@@@@@@@pip @@ common :
def information(url):
    print(f"start {url}")
    #####################
    ydl_opts = {
        'quiet': True,  # تشغيل بدون طباعة رسائل كثيرة
        'noplaylist': True,  # تجنب تحميل قائمة تشغيل بالكامل
        'socket_timeout': 60,  # زيادة مهلة الاتصال
        'geo_bypass': True,  # تجاوز القيود الجغرافية
        'nocheckcertificate': True  # تجاهل مشاكل الشهادات SSL
    }
    with yt_dlp.YoutubeDL(ydl_opts) as yt:
        info_kham = yt.extract_info(url, download=False)  # استخراج المعلومات بدون تحميل
    ######################################
    keys = ['278', '160', '133', '242', '134', '243', '135', '244', '136', '247', '137', '248']
    id_sound = ["139-drc", "249-drc", "250-drc", "139", "249", "250", "140-drc", "251-drc", "140", "251"]
    sounds = {}
    list_format = {}
    for i in range(len(info_kham['formats'])):
        if info_kham['formats'][i]['format_id'] in keys:
            list_format[info_kham['formats'][i]['format_id']] = int(info_kham['formats'][i].get('filesize'))
        if info_kham['formats'][i]['format_id'] in id_sound:
            if info_kham['formats'][i].get('filesize'):
                sounds[info_kham['formats'][i]['format_id']] = info_kham['formats'][i].get('filesize')
    #######################################
    sounds_arranged = dict(sorted(sounds.items(), key=lambda item: item[1]))
    info_video = {
        'v144': {'160': 0, '278':0},
        'v240': {'133':0, '242': 0},
        'v360': {'134': 0, '243': 0},
        'v480': {'135': 0, '244': 0},
        'v720': {'136': 0, '247': 0},
        'v1080': {'137': 0, '248': 0}
    }
    for key, sub_dict in info_video.items():
        for sub_key in sub_dict.keys():
            if sub_key in list_format:
                sub_dict[sub_key] = list_format[sub_key]
    ##########################################
    keys_sub = ['v144', 'v240', 'v360', 'v480', 'v720', 'v1080']

    def small(info):
        # البحث عن المفتاح والقيمة المرتبطة بأقل قيمة
        k, v = min(info.items(), key=lambda item: item[1])
        return [k, v]
    def big(info):
        # البحث عن المفتاح والقيمة المرتبطة بأقل قيمة
        k, v = max(info.items(), key=lambda item: item[1])
        return [k, v]

    ###########################################
    dict_info = {}
    dict_info[list(sounds_arranged.items())[0][0]] = round(list(sounds_arranged.items())[0][1] / (1024 * 1024), 2)
    dict_info[list(sounds_arranged.items())[-1][0]] = round(list(sounds_arranged.items())[-1][1] / (1024 * 1024), 2)
    itags = []
    itags.append(list(sounds_arranged.items())[0][0])
    itags.append(list(sounds_arranged.items())[-1][0])
    for i in range(len(keys_sub)):
        if small(info_video[keys_sub[i]])[1]!=0:
            dict_info[small(info_video[keys_sub[i]])[0]] = (round(small(info_video[keys_sub[i]])[1] / (1024 * 1024), 2))
            itags.append(small(info_video[keys_sub[i]])[0])
        else:
            dict_info[big(info_video[keys_sub[i]])[0]] = (round(big(info_video[keys_sub[i]])[1] / (1024 * 1024), 2))
            itags.append(big(info_video[keys_sub[i]])[0])
    ############################################
    dict_info['title'] = info_kham['title']
    dict_info['itags'] = itags
    dict_info['image'] = info_kham["thumbnail"]
    print(f"finished : {dict_info['title']}")
    return dict_info
    ####################
    ####################
    ####################
##@@@@@@@@@@ one :

def downloading(url, id, path):
    print(id)
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            progress_bar.set(percent / 100)  # تحديث شريط التمرير
            persent.configure(text=f"{round(percent, 2)}%")  # تحديث النسبة المئوية
            filename = d['filename']
            if filename.endswith('.mp4') or filename.endswith('.webm'):  # فيديو
                ext_label.configure(text="الفيديو")
            elif filename.endswith('.m4a') or filename.endswith('.mp3'):  # صوت
                ext_label.configure(text="الصوت")

    options = {  # يجب أن يكون هذا السطر في نفس مستوى التحديد مع `def progress_hook`
        'format': id,
        'outtmpl': path,
        'continue_dl': True,
        'quiet': True,
        'progress_with_newline': False,
        'retries': 60,
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,
        'no_warnings': True,
        'socket_timeout': 60,
        'age_limit': 0,
        'cookies': 'cookies.txt',
        'geo_bypass': True,
        'geo_bypass_country': 'US',
        'referer': 'https://www.youtube.com/',
        'http_headers': {'User-Agent': 'Mozilla/5.0'},
    }

    with yt_dlp.YoutubeDL(options) as file:
        file.download([url])
    print(path)
    if subtitle.get():
        root.title("يتم الآن تنزيل الترجمة")
        download_subtitles(url,path)
        root.title("MG v5.1.0")
        print("finished subtitle")
    ##!@@@@@@@@@


    def open(event):
        if path[-3:]=="mp3":
            os.startfile("H:\downloads\Audio")
        else:
            os.startfile("H:\downloads\Video")
    ##@@@@@@@@@@@

    photo.bind("<Button-1>", lambda event: open(event))

def reset_one():
    persent.configure(text=f"00.00%")
    progress_bar.set(0)
    photo.configure(image=None)
    title_label.configure(text=" سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ")
    ext_label.configure(text="")
    root.title("MG v:5.1.0")
    blaudio.configure(text=f"  Audio :  ",fg_color=default_color,text_color="#EDEDED")
    bhaudio.configure(text=f"  Audio :  ",fg_color=default_color,text_color="#EDEDED")
    #######2#######
    b144p.configure(text=f"  144p  :  ",fg_color=default_color,text_color="#EDEDED")
    b240p.configure(text=f"  240p  :  ",fg_color=default_color,text_color="#EDEDED")
    b360p.configure(text=f"  360p  :  ",fg_color=default_color,text_color="#EDEDED")
    b480p.configure(text=f"  480p  :  ",fg_color=default_color,text_color="#EDEDED")
    b720p.configure(text=f"  720p  :  ",fg_color=default_color,text_color="#EDEDED")
    b1080p.configure(text=f"  1080p :  ",fg_color=default_color,text_color="#EDEDED")
    ####################
def fetch_one(url):
    main_button.configure(text="جاري تحليل الرابط")
    reset_one()
    comlist = [b144p, b240p, b360p, b480p, b720p, b1080p]
    comnames = ['144p', '240p', '360p', '480p', '720p', '1080p']
    info = information(url)

    def chick():
        blaudio.configure(text=f"  Audio : {round(info[info['itags'][0]], 2)} MB")
        bhaudio.configure(text=f"  Audio : {round(info[info['itags'][1]], 2)} MB")
        if not chaudio.get():
            for i, b in enumerate(comlist):
                b.configure(text=f"  {comnames[i]} : غير متاح" if info[info['itags'][i + 2]] ==0 else f"  {comnames[i]} : {round(info[info['itags'][i + 2]] + info[info['itags'][0]], 2)} MB",
                            state='disabled' if info[info['itags'][i + 2]] ==0 else 'normal' )
        else:
            for i, b in enumerate(comlist):
                b.configure(text=f"  {comnames[i]} : غير متاح" if info[info['itags'][i + 2]] == 0 else f"  {comnames[i]} : {round(info[info['itags'][i + 2]] + info[info['itags'][1]], 2)} MB",
                            state='disabled' if info[info['itags'][i + 2]] == 0 else 'normal')

    chick()
    chaudio.configure(command=chick)
    title_label.configure(text=f"{info['title']}")
    root.title(f"{info['title']}")
    path_audio = rf"H:\downloads\Audio\{info['title']}.mp3"
    path_video = rf"H:\downloads\Video\{info['title']}"
    ###############################

    # تعديل الأزرار الصوتية
    blaudio.configure(command=lambda: [
        blaudio.configure(fg_color='#ff8c00',text_color="black"),
        threading.Thread(target=lambda: [
            downloading(url, info['itags'][0], path_audio),
        ]).start()
    ])

    bhaudio.configure(command=lambda: [
        bhaudio.configure(fg_color='#ff8c00',text_color="black"),
        threading.Thread(target=lambda: [
            downloading(url, info['itags'][1], path_audio),
        ]).start()
    ])

    if not chaudio.get():
        b144p.configure(command=lambda: [
            b144p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][0] + '+' + info['itags'][2], path_video),
            ]).start()
        ])

        b240p.configure(command=lambda: [
            b240p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][0] + '+' + info['itags'][3], path_video),
            ]).start()
        ])

        b360p.configure(command=lambda: [
            b360p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][0] + '+' + info['itags'][4], path_video),
            ]).start()
        ])

        b480p.configure(command=lambda: [
            b480p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][0] + '+' + info['itags'][5], path_video),
            ]).start()
        ])

        b720p.configure(command=lambda: [
            b720p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][0] + '+' + info['itags'][6], path_video),
            ]).start()
        ])

        b1080p.configure(command=lambda: [
            b1080p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][0] + '+' + info['itags'][7], path_video),
            ]).start()
        ])

    else:
        b144p.configure(command=lambda: [
            b144p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][1] + '+' + info['itags'][2], path_video),
            ]).start()
        ])

        b240p.configure(command=lambda: [
            b240p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][1] + '+' + info['itags'][3], path_video),
            ]).start()
        ])

        b360p.configure(command=lambda: [
            b360p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][1] + '+' + info['itags'][4], path_video),
            ]).start()
        ])

        b480p.configure(command=lambda: [
            b480p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][1] + '+' + info['itags'][5], path_video),
            ]).start()
        ])

        b720p.configure(command=lambda: [
            b720p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][1] + '+' + info['itags'][6], path_video),
            ]).start()
        ])

        b1080p.configure(command=lambda: [
            b1080p.configure(fg_color='#ff8c00',text_color="black"),
            threading.Thread(target=lambda: [
                downloading(url, info['itags'][1] + '+' + info['itags'][7], path_video),
            ]).start()
        ])

    main_button.configure(text="تحليل رابط التحميل")
    ########photo:
    # تحميل الصورة من الرابط
    def picture():
        from PIL import Image, ImageDraw

        response = requests.get(info["image"])
        img = Image.open(BytesIO(response.content)).resize((240, 120))

        # إنشاء قناع دائري
        mask = Image.new("L", (240, 120), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, 240, 120), radius=15, fill=255)

        # تطبيق القناع لجعل الحواف دائرية
        img.putalpha(mask)

        # تحويل الصورة إلى CTkImage
        ctk_image = ctk.CTkImage(light_image=img, size=(240, 120))

        #photo = ctk.CTkLabel(root, text="", width=220, height=120, corner_radius=15)
        photo.place(x=590, y=505)
        title_label.configure(width=530,wraplength=530)
        photo.configure(image=ctk_image)
    picture()
##@@@@@@@@@@ list :

##########################
def links(url):
    import pytubefix
    y = pytubefix.Playlist(url)
    link = y.video_urls
    title = y.title
    length = y.length
    return [link, title, length]
def download_subtitles(video_url, save_path):
    options = {
        'outtmpl': save_path,  # حفظ الملف كما هو
        "writesubtitles": True,  # تحميل الترجمة الرسمية
        "writeautomaticsub": True,  # تحميل الترجمة التلقائية لو مفيش رسمية
        "subtitleslangs": ["ar"],  # تحديد لغة الترجمة
        "skip_download": True,  # عدم تحميل الفيديو
        "subtitlesformat": "srt",  # تحويل الترجمة إلى SRT
        "quiet": True  # تقليل الإخراج
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_url])

    # البحث عن الترجمة التي تنتهي بـ ".ar.srt" وحذف ".ar"
    for file in os.listdir(os.path.dirname(save_path)):
            old_path = os.path.join(os.path.dirname(save_path), file)
            new_path = re.sub(r"\.ar", "", old_path)  # إزالة .ar
            os.rename(old_path, new_path)

#################
def information_list(urls,s,e):
    print('تم جلب الروابط ')
    print(s,e)
    #################################
    sema = threading.Semaphore(3)
    results = {}  # القاموس لتخزين القيم المرجعة
    threads = []  # قائمة لتخزين الكائنات الخاصة بالثريدات
    for i in range(s-1,e):
        thread = threading.Thread(target=lambda link=urls[i], idx=i: (
        sema.acquire(), results.__setitem__(idx, information(link)), sema.release()))
        thread.start()
        threads.append(thread)  # تخزين الثريد
    # انتظار انتهاء جميع الثريدات قبل طباعة النتائج
    for thread in threads:
        thread.join()
    results = dict(sorted(results.items()))
    return results

    ####################
    ####################

# إنشاء Canvas وشريط التمرير
canvas = ctk.CTkCanvas(root, bg="#1E1E1E")
scrollbar = ctk.CTkScrollbar(root, command=canvas.yview)

###################
def downloading2(url, id, path):
    print(path)
    # إنشاء CTkFrame داخل الـ Canvas
    downframe = ctk.CTkFrame(canvas, width=250, height=200, corner_radius=10, fg_color='#2E2E2E')
    # إظهار الـ CTkFrame في وسط الـ Canvas
    downframe.place(relx=0.5, rely=0.5, anchor="center")
    progress_bar = ctk.CTkProgressBar(downframe, width=500, height=15, corner_radius=4, mode="determinate",
                                      fg_color='#2E2E2E')
    progress_bar.pack(pady=20)
    progress_bar.set(0)
    # ------------
    persent = ctk.CTkLabel(downframe, width=70, height=30, corner_radius=10,text_color='white', text=f"00.00%", font=("", 40, "bold"))
    persent.pack(pady=20)
    #################
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            progress_bar.set(percent / 100)  # تحديث شريط التمرير
            persent.configure(text=f"{round(percent, 2)}%")  # تحديث النسبة المئوية
            ########
            # pr1.set(percent / 100)  # تحديث شريط التمرير
            # per1.configure(text=f"{round(percent, 2)}%")  # تحديث النسبة المئوية

    option = {
        'format': id,  # تحديد كود الجودة المطلوبة
        'outtmpl': path,  # مسار الحفظ
        'continue_dl': True,
        'quiet': True,
        'progress_with_newline': False,
        'retries': 60,
        'progress_hooks': [progress_hook],  # تمرير الـ hook
        'ignoreerrors': True,
        'no_warnings': True,
        'socket_timeout': 60,

        # **تجاوز القيود العمرية والمحتوى المقيد**
        'age_limit': 0,  # تخطي التحقق من العمر
        'cookies': 'cookies.txt',  # استخدم ملف الكوكيز لو الفيديو مقيد بحساب
        # لو مش عايز تستخدم ملف الكوكيز يدويًا، ممكن تجيب الكوكيز من المتصفح مباشرة:
        # 'cookies_from_browser': 'chrome',  # أو 'firefox' حسب المتصفح اللي بتستخدمه

        'geo_bypass': True,  # تجاوز القيود الجغرافية
        'geo_bypass_country': 'US',  # محاكاة موقع أمريكي لتجاوز الحظر
        'referer': 'https://www.youtube.com/',  # تحسين التوافق لبعض الفيديوهات
        'http_headers': {'User-Agent': 'Mozilla/5.0'},  # محاكاة متصفح حقيقي
    }

    with yt_dlp.YoutubeDL(option) as file:
        file.download(url)
    downframe.destroy()
    ####################
    ####################
    ####################
####################
def list_analys(link,s,e):
    # استخراج البيانات من funlinks
    url = link[0]
    title = link[1]
    print(title)
    canvas.delete("all")
    # تكوين Canvas ليعمل مع شريط التمرير
    canvas.configure(yscrollcommand=scrollbar.set)

    # وضع Canvas وشريط التمرير في النافذة الفرعية
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # إنشاء إطار داخلي داخل Canvas
    freminner = ctk.CTkFrame(canvas)
    freminner_window = canvas.create_window((0, 0), window=freminner, anchor="nw", width=canvas.winfo_width())

    # تحديث منطقة التمرير عند تغيير الحجم أو إضافة عناصر
    def update_scroll_region(event=None):
        freminner.update_idletasks()  # تحديث الأبعاد الداخلية
        canvas.configure(scrollregion=canvas.bbox("all"))  # ضبط منطقة التمرير
        canvas.itemconfig(freminner_window, width=canvas.winfo_width())  # تمديد العرض
        canvas.itemconfig(freminner_window, height=freminner.winfo_reqheight())  # ضبط الطول ديناميكيًا

    canvas.bind("<Configure>", update_scroll_region)

    # تحديث التمرير بعد إضافة عناصر جديدة
    root.after(200, update_scroll_region)

    info = information_list(url,s,e)
    x = {}
    sel = {}
    to_down = {}

    def select(cat, index):
        sizeall = 0
        if x[cat][index].get() == 1:  # عند التحديد
            for i, var in enumerate(x[cat]):
                var.set(1 if i == index else 0)  # إلغاء تحديد الباقي
            keys = list(info[cat].keys())  # قائمة بالمفاتيح في الفئة
            #---------
            if index>1:
               selected_key = keys[index]+ '+' +keys[0]
            else:
                selected_key = keys[index]
            if index > 1:
                print(info[cat][keys[0]])
                selected_value = info[cat][keys[index]]+info[cat][keys[0]]
            else:
                selected_value = info[cat][selected_key]
            #---------
            sel[cat] = (index, f"{selected_key} - {selected_value}")
            to_down[cat] = [selected_key, selected_value]
            print(f"k : {cat}  =  id : {selected_key} => v : {selected_value}")
        else:  # لو تم إلغاء التحديد بالكامل
            if cat in to_down:
                del to_down[cat]
        print(to_down)
        for v in to_down.values():
            sizeall+=v[1]
        lab_size.configure(text=f"{round(sizeall,2)} MB")
        #>>>>>>>>>>>>
        def d(url):

            for k, v in to_down.items():
                path = rf"H:\downloads\lists\{title}\%(title)s.mp3"
                if len(str(v[0])) > 3 and v[0][6] != "c":
                    path = rf"H:\downloads\lists\{title}\%(title)s.mp4"
                downloading2(url[k], v[0], path)

        bdown.configure(command=lambda: threading.Thread(target=d, args=(url,)).start())
        #>>>>>>>>>>>>
        return to_down

    res= ['Audio', 'Audio','144p', '240p', '360p', '480p', '720p', '1080p']
    for c, (k, v) in enumerate(info.items()):
        x[k] = []  # قائمة لتخزين المتغيرات بدلاً من متغير واحد لكل فئة
        keys = list(v.keys())
        for i in range(len(keys) - 3):
            var = ctk.IntVar(value=0)
            x[k].append(var)

            cr = ctk.CTkCheckBox(freminner,
                                 text=f" {res[i]} : {round(v[keys[0]]+v[keys[i]],2) if i > 1 else round(v[keys[i]],2)}",
                                 font=('', 10, 'bold'),
                                 variable=var,
                                 command=lambda cat=k, idx=i: select(cat, idx))

            if v[keys[i]] > 0:
                cr.place(x=(i * 120) + 15, y=(c * 70) + 45)  # ترتيب العناصر
            cr.configure(bg_color="#90EE90")

        line = ctk.CTkLabel(freminner, font=('', 15, 'bold'), text=f"\n{c + 1} - {v[keys[8]]} : ", height=25, fg_color="silver",
                            corner_radius=10)
        line.place(x=10, y=(c * 70))  # وضع الخط بين العناصر
        freminner.configure(height=(c * 70) + 100)
    for i in range(2):
        time.sleep(1)
        root.geometry(f"{970+i}x650+300+50")

    #root.geometry("970x650+300+50")
        #>>>>>>>>>>>>>>>>>>
        #>>>>>>>>>>>>>>>>>>
##########
###########
##########
def listoption(y):
    opt=[]
    for  i in range(y):
        opt.append(str(i+1))
    start = ctk.StringVar(value="1")
    end = ctk.StringVar(value=str(y))
    s.configure(values=opt,variable=start,height=40,width=70)
    e.configure(values=opt,variable=end,height=40,width=70)
    print(start.get(),end.get())
    return [start,end]
###############
def scope(start, end):
    # استرجاع القيمة المحددة
    selected_start = int(start.get())  # القيمة المحددة من السلسلة الأولى
    selected_end = int(end.get())  # القيمة المحددة من السلسلة الثانية
    print(f"Start: {selected_start}, End: {selected_end}")
    # إرجاع القيم المحددة
    return [selected_start, selected_end]
##@@@@@@@@@@
def bad_link():
    temp = ctk.CTkFrame(root, width=200, height=100)
    ltemp = ctk.CTkLabel(temp, text="أدخل رابطا صحيحا من فضلك", font=('', 50, 'bold'), fg_color="yellow",
                         text_color="black",corner_radius=15)
    temp.place(x=200, y=300)
    ltemp.pack()
    time.sleep(2)
    temp.destroy()
###########
def main_all():
    print("start main ...")
    url = pyperclip.paste()
    if "youtu" in url:
        if "index" in url:
            url = url.split("&")[0]
        if "list" in url:
            print("start list :")
            forget1()
            link=links(url)
            op=listoption(link[2])
            def info_dict():
                scop = scope(op[0], op[1])
                threading.Thread(target=list_analys, args=(link,scop[0], scop[1])).start()
            banalys.configure(command=info_dict)
        else:
            print("start one :")
            forget2()
            threading.Thread(target=lambda: fetch_one(url)).start()
    else:
        bad_link()

#@@@@@@@@@@@ front_1 :
main_button = ctk.CTkButton(root, text="تحليل رابط التحميل", width=810, height=70, corner_radius=10,
                            font=("", 40, "bold"), command=lambda: threading.Thread(target=main_all).start())
main_button.place(x=45, y=15)
######1#######
blaudio = ctk.CTkButton(root, text=f"  Audio :  ", width=400, height=70, corner_radius=10, font=("", 40, "bold"),
                        anchor="w")
blaudio.place(x=45, y=100)
bhaudio = ctk.CTkButton(root, text=f"  Audio :  ", width=400, height=70, corner_radius=10, font=("", 40, "bold"),
                        anchor="w")
bhaudio.place(x=455, y=100)
#######2#######
b144p = ctk.CTkButton(root, text=f"  144p  :  ", width=400, height=70, corner_radius=10, font=("", 40, "bold"),
                      anchor="w")
b144p.place(x=45, y=185)
b240p = ctk.CTkButton(root, text=f"  240p  :  ", width=400, height=70, corner_radius=10, font=("", 40, "bold"),
                      anchor="w")
b240p.place(x=455, y=185)
#######3#######
b360p = ctk.CTkButton(root, text=f"  360p  :  ", width=400, height=70, corner_radius=10, font=("", 40, "bold"),
                      anchor="w")
b360p.place(x=45, y=270)
b480p = ctk.CTkButton(root, text=f"  480p  :  ", width=400, height=70, corner_radius=10, font=("", 40, "bold"),
                      anchor="w")
b480p.place(x=455, y=270)
#######4########
b720p = ctk.CTkButton(root, text=f"  720p  :  ", width=400, height=70, corner_radius=10, font=("", 40, "bold"),
                      anchor="w")
b720p.place(x=45, y=355)
b1080p = ctk.CTkButton(root, text=f"  1080p :  ", width=400, height=70, corner_radius=10, font=("", 40, "bold"),
                       anchor="w")
b1080p.place(x=455, y=355)
################
photo = ctk.CTkLabel(root, text="", width=220, height=120, corner_radius=15)
###############
##############
progress_bar = ctk.CTkProgressBar(root, width=500, height=15, corner_radius=4, mode="determinate", fg_color='#2E2E2E')
progress_bar.place(x=70, y=457)
progress_bar.set(0)
# ------------
persent = ctk.CTkLabel(root, width=70, height=30, corner_radius=10, text=f"00.00%", font=("", 40, "bold"))
persent.place(x=575, y=440)
# ------------
chaudio = ctk.CTkCheckBox(root, width=70, height=30, corner_radius=10, text=f"ha", font=("", 16, "bold"))
chaudio.place(x=725, y=450)
subtitle= ctk.CTkCheckBox(root, width=70, height=30, corner_radius=10, text=f"ar", font=("", 16, "bold"))
subtitle.place(x=795, y=450)

#################
textd=" سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ"
title_label = ctk.CTkLabel(root, width=800, wraplength=800, corner_radius=10, text=f"{textd}", font=("", 30, "bold"))
title_label.place(x=50, y=500)
ext_label=ctk.CTkLabel(root,width=50,height=20,text="")
ext_label.place(x=425,y=630)
##############
#@@@@@@@@@@@ front_2 :
topframe = ctk.CTkFrame(root, fg_color='#333333', width=370, height=60)
#topframe.pack(side="top", fill='x')
bdown = ctk.CTkButton(topframe, text="تحميل", corner_radius=10, font=('', 30, 'bold'), width=150)
bdown.place(x=10, y=5)
lab_size = ctk.CTkLabel(topframe, text="الحجم الكلي", corner_radius=10, font=('', 35, 'bold'), fg_color="silver",width=150)
lab_size.place(x=175, y=5)
banalys = ctk.CTkButton(topframe, text="تحليل النطاق", corner_radius=10, font=('', 30, 'bold'), width=190)
banalys.place(x=500, y=5)
newlink = ctk.CTkButton(topframe, text="رابط جديد", corner_radius=10, font=('', 30, 'bold'), width=179, command=lambda: threading.Thread(target=main_all).start())
newlink.place(x=700, y=5)
opt=['0']
start = ctk.StringVar(value="0")
end = ctk.StringVar(value="0")
s = ctk.CTkOptionMenu(topframe, values=opt, variable=start, height=40, width=70)
s.place(x=420, y=5)
e = ctk.CTkOptionMenu(topframe, values=opt, variable=end, height=40, width=70)
e.place(x=343, y=5)
def forget1():
    topframe.pack(side="top", fill='x')
    main_button.place_forget()
    blaudio.place_forget()
    bhaudio.place_forget()
    b144p.place_forget()
    b240p.place_forget()
    b360p.place_forget()
    b480p.place_forget()
    b720p.place_forget()
    b1080p.place_forget()
    photo.place_forget()
    ##############
    progress_bar.place_forget()
    persent.place_forget()
    chaudio.place_forget()
    title_label.place_forget()
    ext_label.place_forget()
    ctk.set_appearance_mode("light")  # أو "dark" لو عايز الوضع الليلي

def forget2():
    canvas.pack_forget()
    ctk.set_appearance_mode("dark")  # أو "dark" لو عايز الوضع الليلي
    topframe.pack_forget()
    scrollbar.pack_forget()
    root.geometry("900x650+300+50")
    main_button.place(x=45, y=15)
    blaudio.place(x=45, y=100)
    bhaudio.place(x=455, y=100)
    b144p.place(x=45, y=185)
    b240p.place(x=455, y=185)
    b360p.place(x=45, y=270)
    b480p.place(x=455, y=270)
    b720p.place(x=45, y=355)
    b1080p.place(x=455, y=355)
    progress_bar.place(x=70, y=457)
    persent.place(x=575, y=440)
    chaudio.place(x=725, y=450)
    title_label.place(x=50, y=500)



######################################################################################################
root.mainloop()