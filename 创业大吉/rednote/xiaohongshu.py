from DrissionPage import ChromiumPage, ChromiumOptions
co = ChromiumOptions().set_paths()


co.set_local_port(9743)
# co.add_extension(r'.\proxy_switchyomega-2.5.20-an+fx')
browser = ChromiumPage(co)
browser.get("https://www.xiaohongshu.com/explore")

