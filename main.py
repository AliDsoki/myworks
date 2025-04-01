
################package:
import subprocess
import sys

# Function to install a library
def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except Exception as e:
        print(f"Error installing {package_name}: {e}")

# Check and install libraries
try:
    import tkinter
    from tkinter import ttk
except ImportError:
    install_package("tkinter")  # Usually part of Python, but kept for consistency

try:
    import yt_dlp
except ImportError:
    install_package("yt-dlp")

try:
    import threading  # Standard library, no installation needed
except ImportError:
    print("Threading is a standard library and should be included with Python.")

try:
    import re  # Standard library, no installation needed
except ImportError:
    print("Re is a standard library and should be included with Python.")

try:
    import pytubefix
except ImportError:
    install_package("pytubefix")  # Replace with the correct package name if different


#################
import tkinter
from tkinter import ttk
import yt_dlp
import threading
import re
###############
def one_video(url):
    url = win.clipboard_get()
    bu.config(text='Working ...', foreground='yellow')
    downloadlow.config(text='Audio Low', background='#2E2E2E', foreground='white')
    downloadhigh.config(text='Audio High', background='#2E2E2E', foreground='white')

    try:
        op_yt = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(op_yt) as f:
            info = f.extract_info(url, download=False)

        # Extract itag sizes
        itag_sizes = {}
        for stream in info.get('formats', []):
            if stream.get('format_id') in ['139', '140']:
                filesize = stream.get('filesize', 0) or 0  # Handle None
                itag_sizes[stream.get('format_id')] = filesize / (1024 * 1024)  # MB

        downloadlow.config(text=f'64kbps: {itag_sizes.get("139", "N/A"):.2f} MB')
        downloadhigh.config(text=f'128kbps: {itag_sizes.get("140", "N/A"):.2f} MB')
        bu.config(text='Paste URL', foreground='white')
        lab_title.config(text=info.get("title", "No Title"))

    except Exception as e:
        bu.config(text='Error occurred', foreground='red')
        lab_title.config(text=str(e))

    def progress_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0) or 1  # Avoid division by zero
            downloaded_bytes = d.get('downloaded_bytes', 0) or 0
            percentage = int(downloaded_bytes / total_bytes * 100)
            progress['value'] = percentage
            progress_label.config(text=f'{percentage:02}%')

    def download(ss):
        option = {
            'format': ss,
            'outtmpl': f'%(title)s.mp3',
            'quiet': True,
            'progress_hooks': [progress_hook],
        }

        labd = tkinter.Label(win, text='Downloading...', background='#2E2E2E', foreground='white')
        labd.pack()

        try:
            with yt_dlp.YoutubeDL(option) as file:
                file.download([url])
            labd.config(text='Download complete')
        except Exception as e:
            labd.config(text=f'Error: {e}', foreground='red')

    def dlow():
        threading.Thread(target=lambda: download('139')).start()

    def dhigh():
        threading.Thread(target=lambda: download('140')).start()

    bu.config(text='Paste URL')
    downloadlow.config(command=dlow)
    downloadhigh.config(command=dhigh)
###########################
#######################
run=True
def list_video(url):
    url = win.clipboard_get()
    import pytubefix
    global run
    bu.config(text='Working ...', foreground='yellow')
    downloadlow.config(text='Audio Low', background='#2E2E2E', foreground='white')
    downloadhigh.config(text='Audio High', background='#2E2E2E', foreground='white')
    clip=pytubefix.Playlist(url)
    name=clip.title
    name = re.sub(r'[\/:?\'"]', '', name)
    lab_title.config(text=f"{name}")
    length=clip.length
    options = []
    options.clear()
    for i in range(length):
        options.append(i)
    print(length)
    # تعريف المتغيرات
    print(options)

    # تحديث القيم للقوائم المنسدلة
    start_combobox["values"] = options
    end_combobox["values"] = options
    start_combobox.pack(pady=5)
    # تعيين القيمة الافتراضية
    start_combobox.set(options[0])
    end_combobox.set(options[-1])
    end_combobox.pack(pady=5)
    ###################%%%%%%%%%%%%%%%%%
    def confirming():
        info_list = {}
        itag = [139, 140]
        for i in range(int(start_combobox.get()), int(end_combobox.get()) + 1):
            try:
                info = {}
                current = clip.videos[i].streaming_data
                for x in range(len(current['adaptiveFormats'])):
                    if current['adaptiveFormats'][x]['itag'] in itag:
                        info[current['adaptiveFormats'][x]['itag']] = round(int(current['adaptiveFormats'][x]['contentLength']) / 1049000, 2)
                info_list[i] = info
            except:
                print('no')

        #########
        print(info_list)
        size = {139: 0, 140: 0}
        for i in range(int(start_combobox.get()), int(end_combobox.get()) + 1):
                for a, b in info_list[i].items():
                    size[a] += b
        downloadlow.config(text=f"{round(size[139],2)} MB")  # عرض الحجم بالميجابايت
        downloadhigh.config(text=f"{round(size[140],2)} MB")  # عرض الحجم بالميجابايت

    ##########
    confirm.config(command=lambda :threading.Thread(target=confirming).start())
    confirm.pack(pady=5)
    def progress_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0) or 1  # Avoid division by zero
            downloaded_bytes = d.get('downloaded_bytes', 0) or 0
            percentage = int(downloaded_bytes / total_bytes * 100)
            progress['value'] = percentage
            progress_label.config(text=f'{percentage:02}%')

    def download(ss):
        option = {
            'format': ss,
            'outtmpl': rf'\{name}\%(title)s.mp3',
            'quiet': True,
            'progress_hooks': [progress_hook],
        }

        labd = tkinter.Label(win, text='Downloading...', background='#2E2E2E', foreground='white')
        labd.pack(pady=3)

        for i in range(int(start_combobox.get()), int(end_combobox.get()) + 1):
            lab_title.config(text=f'{clip.videos[i].title}')
            with yt_dlp.YoutubeDL(option) as file:
                file.download([clip.video_urls[i]])
        lab_title.config(text="complete")


    def dlow():
        threading.Thread(target=lambda: download('139')).start()

    def dhigh():
        threading.Thread(target=lambda: download('140')).start()

    bu.config(text='Paste URL')
    downloadlow.config(command=dlow)
    downloadhigh.config(command=dhigh)
######################
#####################
def pick():
    url = win.clipboard_get()
    return url
def main_download():
    url=pick()
    if 'list' in url:
        list_video(url)
    else:
        one_video(url)


# Initialize Tkinter window
win = tkinter.Tk()
win.title('Media Graper')
win.config(background='#2E2E2E')
# Widgets
bu = tkinter.Button(win, text='Paste URL', command=lambda: threading.Thread(target=main_download).start(),
                    font=('', 20, 'bold'), background='#2E2E2E', foreground='white')
bu.pack(pady=10)

progress = ttk.Progressbar(win, orient='horizontal', length=300, mode='determinate')
progress.pack(pady=5)

progress_label = tkinter.Label(win, text='00%', font=('', 20, 'bold'), background='#2E2E2E', foreground='white')
progress_label.pack()
########

########
downloadlow = tkinter.Button(win, text='Audio Low', font=('', 20, 'bold'), background='#2E2E2E', foreground='white')
downloadlow.pack(pady=10)

downloadhigh = tkinter.Button(win, text='Audio High', font=('', 20, 'bold'), background='#2E2E2E', foreground='white')
downloadhigh.pack(pady=10)

lab_title = tkinter.Label(win, text='', font=('', 15, 'bold'), wraplength=700, background='#2E2E2E', foreground='yellow')
lab_title.pack(pady=5)

###########
start_combobox = ttk.Combobox(win, values=[])
end_combobox = ttk.Combobox(win, values=[])
############
confirm=tkinter.Button(win,text='confirm', font=('', 20, 'bold'), background='#2E2E2E', foreground='white')
win.mainloop()
