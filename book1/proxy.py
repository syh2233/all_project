
import platform
import random
from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger


def switch_ip(colist):
    global set_proxy
    if ips:
        # 设置proxy
        ip, port, username, password = ips.split(":")
        if colist == 1:
            tab1 = browser1.new_tab()
            tab1.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1 < 2:
                try:
                    tab1.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab1.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab1.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab1.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab1.ele('@ng-model:model').input(username, clear=True)
            except:
                tab1.close()
                tab1 = browser1.new_tab()
                tab1.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1 < 2:
                    try:
                        tab1.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab1.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab1.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab1.ele('@class:glyphicon glyphicon-lock').click()
                tab1.ele('@ng-model:model').input(username, clear=True)
                tab1.ele('@name:password').input(password, clear=True)
                tab1.ele('@class:btn btn-primary ng-binding').click()
                tab1.wait(1)
                tab1.ele('x://a[@ng-click="applyOptions()"]').click()
                tab1.wait(1)
                tab1.close()
                tab = browser1.new_tab()
                tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                tab.ele('@class:om-nav-item om-active').click()
                if len(browser1.tab_ids) > 1:
                    print("当前tab个数", len(browser1.tab_ids))
                    tab.close()
                return
            tab1.ele('@name:password').input(password, clear=True)
            tab1.ele('@class:btn btn-primary ng-binding').click()
            tab1.wait(1)
            tab1.ele('x://a[@ng-click="applyOptions()"]').click()
            tab1.wait(1)
            tab1.close()
            tab1 = browser1.new_tab()
            tab1.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab1.ele('x://span[text()="proxy"]').click()
                    break
                except:
                    tab1.close()
                    tab1 = browser1.new_tab()
                    tab1.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser1.tab_ids) > 1:
                print("当前tab个数", len(browser1.tab_ids))
                tab1.close()
        elif colist == 2:
            tab2 = browser2.new_tab()
            tab2.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1 < 2:
                try:
                    tab2.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab2.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab2.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab2.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab2.ele('@ng-model:model').input(username, clear=True)
            except:
                tab2.close()
                tab2 = browser2.new_tab()
                tab2.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1 < 2:
                    try:
                        tab2.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab2.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab2.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab2.ele('@class:glyphicon glyphicon-lock').click()
                tab2.ele('@ng-model:model').input(username, clear=True)
                tab2.ele('@name:password').input(password, clear=True)
                tab2.ele('@class:btn btn-primary ng-binding').click()
                tab2.wait(1)
                tab2.ele('x://a[@ng-click="applyOptions()"]').click()
                tab2.wait(1)
                tab2.close()
                tab2 = browser2.new_tab()
                tab2.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                while 1 < 2:
                    try:
                        tab2.ele('x://span[text()="proxy"]').click()

                        break
                    except:
                        tab2.close()
                        tab2 = browser2.new_tab()
                        tab2.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                if len(browser2.tab_ids) > 1:
                    print("当前tab个数", len(browser2.tab_ids))
                    tab2.close()
                return
            tab2.ele('@name:password').input(password, clear=True)
            tab2.ele('@class:btn btn-primary ng-binding').click()
            tab2.wait(1)
            tab2.ele('x://a[@ng-click="applyOptions()"]').click()
            tab2.wait(1)
            tab2.close()
            tab2 = browser2.new_tab()
            tab2.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab2.ele('x://span[text()="proxy"]').click()
                    break
                except:
                    tab2.close()
                    tab2 = browser2.new_tab()
                    tab2.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser2.tab_ids) > 1:
                print("当前tab个数", len(browser2.tab_ids))
                tab2.close()
        elif colist == 3:
            tab3 = browser3.new_tab()
            tab3.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1 < 2:
                try:
                    tab3.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab3.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab3.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab3.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab3.ele('@ng-model:model').input(username, clear=True)
            except:
                tab3.close()
                tab3 = browser3.new_tab()
                tab3.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1<2:
                    try:
                        tab3.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab3.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab3.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab3.ele('@class:glyphicon glyphicon-lock').click()
                tab3.ele('@ng-model:model').input(username, clear=True)
                tab3.ele('@name:password').input(password, clear=True)
                tab3.ele('@class:btn btn-primary ng-binding').click()
                tab3.wait(1)
                tab3.ele('x://a[@ng-click="applyOptions()"]').click()
                tab3.wait(1)
                tab3.close()
                tab3 = browser3.new_tab()
                tab3.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                while 1 < 2:
                    try:
                        tab3.ele('x://span[text()="proxy"]').click()

                        break
                    except:
                        tab3.close()
                        tab3 = browser3.new_tab()
                        tab3.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                if len(browser3.tab_ids) > 1:
                    print("当前tab个数", len(browser3.tab_ids))
                    tab3.close()
                return
            tab3.ele('@name:password').input(password, clear=True)
            tab3.ele('@class:btn btn-primary ng-binding').click()
            tab3.wait(1)
            tab3.ele('x://a[@ng-click="applyOptions()"]').click()
            tab3.wait(1)
            tab3.close()
            tab3 = browser3.new_tab()
            tab3.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab3.ele('x://span[text()="proxy"]').click()

                    break
                except:
                    tab3.close()
                    tab3 = browser3.new_tab()
                    tab3.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser3.tab_ids) > 1:
                print("当前tab个数", len(browser3.tab_ids))
                tab3.close()
        elif colist == 4:
            tab4 = browser4.new_tab()
            tab4.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1<2:
                try:
                    tab4.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab4.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab4.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab4.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab4.ele('@ng-model:model').input(username, clear=True)
            except:
                tab4.close()
                tab4 = browser4.new_tab()
                tab4.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1<2:
                    try:
                        tab4.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab4.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab4.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab4.ele('@class:glyphicon glyphicon-lock').click()
                tab4.ele('@ng-model:model').input(username, clear=True)
                tab4.ele('@name:password').input(password, clear=True)
                tab4.ele('@class:btn btn-primary ng-binding').click()
                tab4.wait(1)
                tab4.ele('x://a[@ng-click="applyOptions()"]').click()
                tab4.wait(1)
                tab4.close()
                tab4 = browser4.new_tab()
                tab4.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                while 1 < 2:
                    try:
                        tab4.ele('x://span[text()="proxy"]').click()

                        break
                    except:
                        tab4.close()
                        tab4 = browser4.new_tab()
                        tab4.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                if len(browser4.tab_ids) > 1:
                    print("当前tab个数", len(browser4.tab_ids))
                    tab4.close()
                return
            tab4.ele('@name:password').input(password, clear=True)
            tab4.ele('@class:btn btn-primary ng-binding').click()
            tab4.wait(1)
            tab4.ele('x://a[@ng-click="applyOptions()"]').click()
            tab4.wait(1)
            tab4.close()
            tab4 = browser4.new_tab()
            tab4.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab4.ele('x://span[text()="proxy"]').click()
                    break
                except:
                    tab4.close()
                    tab4 = browser4.new_tab()
                    tab4.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser4.tab_ids) > 1:
                print("当前tab个数", len(browser4.tab_ids))
                tab4.close()
        elif colist == 5:
            tab5 = browser5.new_tab()
            tab5.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1<2:
                try:
                    tab5.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab5.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab5.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab5.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab5.ele('@ng-model:model').input(username, clear=True)
            except:
                tab5.close()
                tab5 = browser5.new_tab()
                tab5.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1 < 2:
                    try:
                        tab5.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab5.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab5.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab5.ele('@class:glyphicon glyphicon-lock').click()
                tab5.ele('@ng-model:model').input(username, clear=True)
                tab5.ele('@name:password').input(password, clear=True)
                tab5.ele('@class:btn btn-primary ng-binding').click()
                tab5.wait(1)
                tab5.ele('x://a[@ng-click="applyOptions()"]').click()
                tab5.wait(1)
                tab5.close()
                tab5 = browser5.new_tab()
                tab5.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                while 1 < 2:
                    try:
                        tab5.ele('x://span[text()="proxy"]').click()
                        break
                    except:
                        tab5.close()
                        tab5 = browser5.new_tab()
                        tab5.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                if len(browser5.tab_ids) > 1:
                    print("当前tab个数", len(browser5.tab_ids))
                    tab5.close()
                return
            tab5.ele('@name:password').input(password, clear=True)
            tab5.ele('@class:btn btn-primary ng-binding').click()
            tab5.wait(1)
            tab5.ele('x://a[@ng-click="applyOptions()"]').click()
            tab5.wait(1)
            tab5.close()
            tab5 = browser5.new_tab()
            tab5.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab5.ele('x://span[text()="proxy"]').click()
                    break
                except:
                    tab5.close()
                    tab5 = browser5.new_tab()
                    tab5.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser5.tab_ids) > 1:
                print("当前tab个数", len(browser5.tab_ids))
                tab5.close()
        elif colist == 6:
            tab6 = browser6.new_tab()
            tab6.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1 < 2:
                try:
                    tab6.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab6.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab6.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab6.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab6.ele('@ng-model:model').input(username, clear=True)
            except:
                tab6.close()
                tab6 = browser6.new_tab()
                tab6.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1 < 2:
                    try:
                        tab6.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab6.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab6.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab6.ele('@class:glyphicon glyphicon-lock').click()
                tab6.ele('@ng-model:model').input(username, clear=True)
                tab6.ele('@name:password').input(password, clear=True)
                tab6.ele('@class:btn btn-primary ng-binding').click()
                tab6.wait(1)
                tab6.ele('x://a[@ng-click="applyOptions()"]').click()
                tab6.wait(1)
                tab6.close()
                tab6 = browser6.new_tab()
                tab6.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                while 1 < 2:
                    try:
                        tab6.ele('x://span[text()="proxy"]').click()

                        break
                    except:
                        tab6.close()
                        tab6 = browser6.new_tab()
                        tab6.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                if len(browser6.tab_ids) > 1:
                    print("当前tab个数", len(browser6.tab_ids))
                    tab6.close()
                return
            tab6.ele('@name:password').input(password, clear=True)
            tab6.ele('@class:btn btn-primary ng-binding').click()
            tab6.wait(1)
            tab6.ele('x://a[@ng-click="applyOptions()"]').click()
            tab6.wait(1)
            tab6.close()

            tab6 = browser6.new_tab()
            tab6.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab6.ele('x://span[text()="proxy"]').click()
                    break
                except:
                    tab6.close()
                    tab6 = browser6.new_tab()
                    tab6.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser6.tab_ids) > 1:
                print("当前tab个数", len(browser6.tab_ids))
                tab6.close()
        elif colist == 7:
            tab7 = browser7.new_tab()
            tab7.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1<2:
                try:
                    tab7.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab7.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab7.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab7.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab7.ele('@ng-model:model').input(username, clear=True)
            except:
                tab7.close()
                tab7 = browser7.new_tab()
                tab7.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1 < 2:
                    try:
                        tab7.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab7.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab7.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab7.ele('@class:glyphicon glyphicon-lock').click()
                tab7.ele('@ng-model:model').input(username, clear=True)
                tab7.ele('@name:password').input(password, clear=True)
                tab7.ele('@class:btn btn-primary ng-binding').click()
                tab7.wait(1)
                tab7.ele('x://a[@ng-click="applyOptions()"]').click()
                tab7.wait(1)

                tab7.close()

                tab7 = browser7.new_tab()
                tab7.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                while 1 < 2:
                    try:
                        tab7.ele('x://span[text()="proxy"]').click()
                        break
                    except:
                        tab7.close()
                        tab7 = browser7.new_tab()
                        tab7.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                if len(browser7.tab_ids) > 1:
                    print("当前tab个数", len(browser7.tab_ids))
                    tab7.close()
                return
            tab7.ele('@name:password').input(password, clear=True)
            tab7.ele('@class:btn btn-primary ng-binding').click()
            tab7.wait(1)
            tab7.ele('x://a[@ng-click="applyOptions()"]').click()
            tab7.wait(1)
            tab7.close()
            tab7 = browser7.new_tab()
            tab7.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab7.ele('x://span[text()="proxy"]').click()
                    break
                except:
                    tab7.close()
                    tab7 = browser7.new_tab()
                    tab7.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser7.tab_ids) > 1:
                print("当前tab个数", len(browser7.tab_ids))
                tab7.close()
        elif colist == 8:
            tab8 = browser8.new_tab()
            tab8.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1 <2:
                try:
                    tab8.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab8.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab8.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab8.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab8.ele('@ng-model:model').input(username, clear=True)
            except:
                tab8.close()
                tab8 = browser8.new_tab()
                tab8.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1 < 2:
                    try:
                        tab8.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab8.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab8.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab8.ele('@class:glyphicon glyphicon-lock').click()
                tab8.ele('@ng-model:model').input(username, clear=True)
                tab8.ele('@name:password').input(password, clear=True)
                tab8.ele('@class:btn btn-primary ng-binding').click()
                tab8.wait(1)
                tab8.ele('x://a[@ng-click="applyOptions()"]').click()
                tab8.wait(1)
                tab8.close()
                tab8 = browser8.new_tab()
                tab8.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                while 1 < 2:
                    try:
                        tab8.ele('x://span[text()="proxy"]').click()
                        break
                    except:
                        tab8.close()
                        tab8 = browser8.new_tab()
                        tab8.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                if len(browser8.tab_ids) > 1:
                    print("当前tab个数", len(browser8.tab_ids))
                    tab8.close()
                return
            tab8.ele('@name:password').input(password, clear=True)
            tab8.ele('@class:btn btn-primary ng-binding').click()
            tab8.wait(1)
            tab8.ele('x://a[@ng-click="applyOptions()"]').click()
            tab8.wait(1)
            tab8.close()
            tab8 = browser8.new_tab()
            tab8.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab8.ele('x://span[text()="proxy"]').click()
                    break
                except:
                    tab8.close()
                    tab8 = browser8.new_tab()
                    tab8.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser8.tab_ids) > 1:
                print("当前tab个数", len(browser8.tab_ids))
                tab8.close()
        elif colist == 9:
            tab9 = browser9.new_tab()
            tab9.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1 < 2:
                try:
                    tab9.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab9.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab9.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab9.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab9.ele('@ng-model:model').input(username, clear=True)
            except:
                tab9.close()
                tab9 = browser9.new_tab()
                tab9.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1 < 2:
                    try:
                        tab9.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab9.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab9.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab9.ele('@class:glyphicon glyphicon-lock').click()
                tab9.ele('@ng-model:model').input(username, clear=True)
                tab9.ele('@name:password').input(password, clear=True)
                tab9.ele('@class:btn btn-primary ng-binding').click()
                tab9.wait(1)
                tab9.ele('x://a[@ng-click="applyOptions()"]').click()
                tab9.wait(1)
                tab9.close()
                tab9 = browser9.new_tab()
                tab9.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                while 1 < 2:
                    try:
                        tab9.ele('x://span[text()="proxy"]').click()
                        break
                    except:
                        tab9.close()
                        tab9 = browser9.new_tab()
                        tab9.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                if len(browser9.tab_ids) > 1:
                    print("当前tab个数", len(browser9.tab_ids))
                    tab9.close()
                return
            tab9.ele('@name:password').input(password, clear=True)
            tab9.ele('@class:btn btn-primary ng-binding').click()
            tab9.wait(1)
            tab9.ele('x://a[@ng-click="applyOptions()"]').click()
            tab9.wait(1)
            tab9.close()
            tab9 = browser9.new_tab()
            tab9.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab9.ele('x://span[text()="proxy"]').click()
                    break
                except:
                    tab9.close()
                    tab9 = browser9.new_tab()
                    tab9.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser9.tab_ids) > 1:
                print("当前tab个数", len(browser9.tab_ids))
                tab9.close()
        elif colist == 10:
            tab10 = browser10.new_tab()
            tab10.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            while 1 < 2:
                try:
                    tab10.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                    break
                except:
                    tab10.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
            tab10.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
            tab10.ele('@class:glyphicon glyphicon-lock').click()
            try:
                tab10.ele('@ng-model:model').input(username, clear=True)
            except:
                tab10.close()
                tab10 = browser10.new_tab()
                tab10.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                while 1 <2:
                    try:
                        tab10.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
                        break
                    except:
                        tab10.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
                tab10.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
                tab10.ele('@class:glyphicon glyphicon-lock').click()
                tab10.ele('@ng-model:model').input(username, clear=True)
                tab10.ele('@name:password').input(password, clear=True)
                tab10.ele('@class:btn btn-primary ng-binding').click()
                tab10.wait(1)
                tab10.ele('x://a[@ng-click="applyOptions()"]').click()
                tab10.wait(1)
                tab10.close()
                tab10 = browser10.new_tab()
                tab10.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                while 1 < 2:
                    try:
                        tab10.ele('x://span[text()="proxy"]').click()
                        break
                    except:
                        tab10.close()
                        tab10 = browser10.new_tab()
                        tab10.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
                if len(browser10.tab_ids) > 1:
                    print("当前tab个数", len(browser10.tab_ids))
                    tab10.close()
                return
            tab10.ele('@name:password').input(password, clear=True)
            tab10.ele('@class:btn btn-primary ng-binding').click()
            tab10.wait(1)
            tab10.ele('x://a[@ng-click="applyOptions()"]').click()
            tab10.wait(1)
            tab10.close()
            tab10 = browser10.new_tab()
            tab10.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            while 1 < 2:
                try:
                    tab10.ele('x://span[text()="proxy"]').click()
                    break
                except:
                    tab10.close()
                    tab10 = browser10.new_tab()
                    tab10.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            if len(browser10.tab_ids) > 1:
                print("当前tab个数", len(browser10.tab_ids))
                tab10.close()


# 3、随机切换代理ip
def proxy_pool(colist):
    global ips
    math = random.randint(100, 1000000)
    list1 = []
    list1.append(f'174.138.174.154:7383:LV16795954-LV1659893070-{math}:122d4e1c86')
    ips = list1[0]
    ip1, port1, username1, password1 = ips.split(":")
    logger.info(f"~~~切换ip，now {ip1}")
    # 重置switchyOmega插件
    switch_ip(colist)
    # browser.wait(1)
    try:
        if colist == 1:
            browser1.get("https://www.ip38.com/", retry=0)
        elif colist == 2:
            browser2.get("https://www.ip38.com/", retry=0)
        elif colist == 3:
            browser3.get("https://www.ip38.com/", retry=0)
        elif colist == 4:
            browser4.get("https://www.ip38.com/", retry=0)
        elif colist == 5:
            browser5.get("https://www.ip38.com/", retry=0)
        elif colist == 6:
            browser6.get("https://www.ip38.com/", retry=0)
        elif colist == 7:
            browser7.get("https://www.ip38.com/", retry=0)
        elif colist == 8:
            browser8.get("https://www.ip38.com/", retry=0)
        elif colist == 9:
            browser9.get("https://www.ip38.com/", retry=0)
        elif colist == 10:
            browser10.get("https://www.ip38.com/", retry=0)
        logger.success(f">>>>>>>>切换代理成功{math}")
    except Exception as err:
        logger.error(f"----------切换代理失败 dp {err}")

if __name__ == "__main__":
    a = 1
    colist = 10
    if a == 1:
        co = ChromiumOptions().set_paths()
        # browser_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    else:
        co = ChromiumOptions().set_paths()
    # co.headless(True)
    co.set_timeouts(6, 6, 6)
    co1 = ChromiumOptions().set_local_port(9222)
    # 1、设置switchyOmega插件
    co.add_extension(r'C:\Users\沈家\Downloads\proxy_switchyomega-2.5.20-an+fx')
    browser1 = ChromiumPage(co)
    browser2 = ChromiumPage(co)
    browser3 = ChromiumPage(co)
    browser4 = ChromiumPage(co)
    browser5 = ChromiumPage(co)
    browser6 = ChromiumPage(co)
    browser7 = ChromiumPage(co)
    browser8 = ChromiumPage(co)
    browser9 = ChromiumPage(co)
    browser10 = ChromiumPage(co)
    proxy_pool(colist)