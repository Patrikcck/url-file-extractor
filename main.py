import threading, requests, os

def download_file(url, filename):
    global progress
    r = requests.get(url)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(r.text)
    with progress_lock:
        progress += 1
        os.system('cls')
        print(progress_update())
    
        
threads = []
progress = 0
l = 0
progress_lock = threading.Lock()

def progress_update():
    global l
    global progress
    s = '['
    for i in range(l):
        if i < progress:
            s += '/'
        else:
            s += '-'
    s += ']'
    return s

def init_stats():
    with open('statistics.txt', 'w') as stats:
        stats.write("Nr.     File Name     Words     P Words     Y Words     T Words     H Words     O Words     N Words\n")

"""       
def count_words(filename, possible_first_letters, total_word_count: bool = True):
    length = len(possible_first_letters)
    stats = [0] * length
    try:
        with open(filename, 'r', encoding = "utf8") as f:
            data = f.read()
            if data[0] == '\ufeff':
                data = data[1:]

            words = data.split()
            for word in words:
                word = word.strip()
                first = word[0].lower()
                for i in range(length):
                    if first == possible_first_letters[i]:
                        stats[i] += 1
                        break
            if total_word_count:
                stats.append(len(words))
        return stats
    except Exception as e:
        print(f"Could not read {filename}: {e}")
"""
def count_words(filename, possible_first_letters, total_word_count: bool = True):
    length = len(possible_first_letters)
    stats = [0] * length
    try:
        with open(filename, 'r', encoding = "utf8") as f:
            data = f.read()
            if data[0] == '\ufeff':
                data = data[1:]

            words = data.split()
            i = 0
            for letter in possible_first_letters:
                w = filter(lambda x: x[0].lower() == letter, words)
                stats[i] = len(list(w))
                i += 1
            if total_word_count:
                stats.append(len(words))
        return stats
    except Exception as e:
        print(f"Could not read {filename}: {e}")
    

def main():
    with open('urls.txt') as file:
        lines = file.readlines()
    global l
    l = len(lines)
    for i in range(l):
        thread = threading.Thread(target=download_file, args=(lines[i].strip(), f'file{i}'))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
    init_stats()
    with open('statistics.txt', 'a') as stats:
        for i in range(l):
            info = count_words(f'file{i}', 'python')
            stats.write(f'{i:<7} {f"file{i}":<13} {info[-1]:<10}')
            for i in range(len(info) - 1):
                stats.write(f'{info[i]:<12}')
            stats.write('\n')
            
        
if __name__ == '__main__':
    main()