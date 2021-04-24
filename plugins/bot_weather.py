import base64
import const
import time
import requests

from botoy import Action, GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, in_content, these_msgtypes
from botoy.refine import refine_pic_group_msg
from botoy.sugar import Text

@ignore_botself
@these_msgtypes(MsgTypes.TextMsg)
@in_content(const.PREFIX + "(云图|预报)")
def receive_group_msg(ctx: GroupMsg):
    try:
        if ctx.Content.startswith(const.PREFIX + "云图"):
            text = ctx.Content[3:].lstrip()
            if text == "":
                Text(const.BOTNAME + "现已支持的云图\n风云二号全国云图: {0}云图 fy2\n风云二号西北太平洋云图: {0}云图 fy2f\n风云四号全国云图: {0}云图 fy4a\n风云四号全圆盘云图: {0}云图 fy4af\n向日葵8号机动观测：{0}云图 h8".format(const.PREFIX))
                return

            cloud_atlas_list = {
                "fy2": cloud_atlas.fy2,
                "fy2f": cloud_atlas.fy2f,
                "fy4a": cloud_atlas.fy4a,
                "fy4af": cloud_atlas.fy4af,
                "h8": cloud_atlas.h8
            }

            if text in cloud_atlas_list:
                pic_url = cloud_atlas_list.get(text)()
                Action(ctx.CurrentQQ).sendGroupPic(
                    ctx.FromGroupId,
                    picUrl = pic_url
                )
            else:
                Text(const.BOTNAME + "没有此类云图")
        elif ctx.Content.startswith(const.PREFIX + "预报"):
            text = ctx.Content[3:].lstrip()
            if text == "":
                text = "24"

            weather_forecast_list = {
                "24": weather_forecast.hour_pic("24"),
                "48": weather_forecast.hour_pic("48"),
                "72": weather_forecast.hour_pic("72")
            }

            if text in weather_forecast_list:
                pic_url = weather_forecast_list.get(text)
                if pic_url == None:
                    Text("今日还没有{}小时降水量预报图，请6点后再试".format(text))
                else:
                    Action(ctx.CurrentQQ).sendGroupPic(
                    ctx.FromGroupId,
                    picUrl = pic_url
                )

    except BaseException as err:
        Text("执行指令时出错：\n{}\nline {}: {}".format(
        err.__traceback__.tb_frame.f_globals["__file__"],
        err.__traceback__.tb_lineno,
        err))

class cloud_atlas():

    gm_time = time.strftime("%Y%m%d", time.gmtime())
    hour = time.gmtime().tm_hour
    minute = time.gmtime().tm_min

    @staticmethod
    def fy2():
        if cloud_atlas.hour == 1 or cloud_atlas.hour == 2:
            hour = 16
        elif cloud_atlas.minute < 30:
            hour = cloud_atlas.hour - 1
        
        url = "http://img.nsmc.org.cn/CLOUDIMAGE/FY2/WXCL/SEVP_NSMC_WXCL_ASC_E99_ACHN_LNO_PY_{}{}1500000.jpg".format(cloud_atlas.gm_time, "%02d" % hour) #中国气象局源
        return url

    @staticmethod
    def fy2f():
        url = "http://img.nsmc.org.cn/CLOUDIMAGE/FY2F/REG/FY2F_SEC_IR1_PA5_YYYYMMDD_HHmm.jpg" #国家卫星气象中心源
        return url

    @staticmethod
    def fy4a():
        url = "http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_CHINA.JPG" #国家卫星气象中心源
        return url

    @staticmethod
    def fy4af():
        url = "http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_DISK.JPG" #国家卫星气象中心源
        return url

    @staticmethod
    def h8():
        if -2 < cloud_atlas.hour < 9:
            url = "https://weather-models.info/latest/nocache/himawari/target/vis0.png" #WeatherModels源 真彩色
        else:
            url = "https://weather-models.info/latest/nocache/himawari/target/bd0.png" #WeatherModels源 红外
        return url

class weather_forecast():

    local_time = time.strftime("%Y%m%d", time.localtime())
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min

    @staticmethod
    def hour_pic(hour):
        if 5 >= weather_forecast.hour >= 0:
            return None
        elif 17 >= weather_forecast.hour > 5:
            url = "https://pi.weather.com.cn/i/product/pic/l/sevp_nmc_stfc_sfer_er24_achn_l88_p9_{}00000{}00.jpg".format(weather_forecast.local_time, hour)
        elif weather_forecast.hour > 17:
            url = "https://pi.weather.com.cn/i/product/pic/l/sevp_nmc_stfc_sfer_er24_achn_l88_p9_{}121000{}00.jpg".format(weather_forecast.local_time, hour)

        return url