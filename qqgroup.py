import requests,random
from os import listdir
import os,re
import urllib3
class GenQQMem:
    group_url='https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'#获取群信息的url，这里用类变量，因为他不会变
    def __init__(self,qq_num,group_name='',mem_count=20):
        self.qq_num=qq_num #qq号码，这里绑定之后，下面就可以self使用了
        self.mem_count=mem_count #成员数量，默认获取20个
        self.dir_name=qq_num+'_'+group_name #这个是每个群的文件夹，用群号+群名字做文件夹的名字，存放每个群里人的头像
 
    def Foma(self,data):#将data格式变成字典格式
        dic = {}
        dat = data.split('&')
        for d in dat:
            d = d.replace('=', ':')
            d1 = d.split(':')[0]
            dic[d1] = d.split(':')[1]
        return dic
    def get_mems(self):
        #这个函数用来下载所有的头像，获取所有的qq成员信息
        #发送post请求，获取到所有群成员信息
        all_nicks=[]
        for i in range(0,2000,20):# 默认20 ，2000号
            data='gc=%s&st=%s&end=%s&sort=0&bkn=1608777410'%(self.qq_num,i,i+self.mem_count)#这个是请求数据
            m=self.Foma(data)
            cookies={
                'Cookie': 'pgv_pvi=9456217088; RK=XOrk2T7yZQ; ptcz=7beebe8cf154d2e2ae7a7b98b0096e1a2036807d0b54c90f91c0adb33c447abe; _ga=GA1.2.948016795.1591761068; pgv_pvid=3493788426; tvfe_boss_uuid=9d02bc06a2e45827; pac_uid=0_ca21ab9494274; pgv_info=ssid=s6535202992; verifysession=h011cc84b32bf461cc304c69dd9c7d7af60c33090379c028c336dcb331c1e62d68910e2319f29f71dd8; _qpsvr_localtk=0.43468354784382224; uin=o0280938995; skey=@N4M6aXiNH; p_uin=o0280938995; pt4_token=Y-BtrT2yzGgfFoYTpAymmNKqni3eU7lthSG1-WTuwD8_; p_skey=zHqc1n4O3kRWlHIAu*U0Uv9OozIYfcpDFWxNWChDNcw_;'
            }#cookie信息，浏览器里面复制的
            requests.packages.urllib3.disable_warnings()
            res=requests.post(self.group_url,data=m,headers=cookies,verify=False).json()##发送post请求，传入cookie和data
            print(res)
            mems=res.get('mems')#mems这个key里面存的是一个list，所有的qq群成员在这里
            if not os.path.isdir(self.dir_name):#判断这个群的文件夹是否存在，如果不存的话，创建
                os.mkdir(self.dir_name)
            for m in mems:
                url='https://q4.qlogo.cn/g?b=qq&nk={}&s=140'.format(m.get('uin')) #通过替换qq号，生成每个qq成员的头像url
                abs_path = os.path.join(self.dir_name, '%s.jpg' % m.get('uin'))  # 拼好每个图片的绝对路径，以qq号命名       
                nick_name = m.get('nick')  # 昵称
                print('下载完成【%s】' % nick_name)  # 打印提示
                all_nicks.append(nick_name)  # 把所有的昵称保存到一个list里面，用来做词云
        return all_nicks  # 返回所有的昵称list
 
    def clear_nicks(self, nicks):
 
        return [re.sub('&.*?;', '', nick) for nick in nicks]
        # 因为有的人昵称里面有空格，空格是html标签
        # 出来就是这样的 快乐  小猪
        # 或者有大于号的就是这样的 天天>开心
        # 这里用正则表达式，把&xx;这样的字符串都替换成空
 

 
    def main(self):
        # 入口
        all_nicks = self.get_mems()  # 调用获取获取成员信息、下载图片接口
        all_nicks = self.clear_nicks(all_nicks)
        
if __name__=='__main__':
    q = GenQQMem('436516199', '腾讯云视频云（直播&点播）产品技术交流群2')#实例化
    q.main()#调用