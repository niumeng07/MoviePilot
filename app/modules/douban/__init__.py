from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Union

from app.core.config import settings
from app.core.context import MediaInfo
from app.core.meta import MetaBase
from app.core.metainfo import MetaInfo
from app.log import logger
from app.modules import _ModuleBase
from app.modules.douban.apiv2 import DoubanApi
from app.modules.douban.scraper import DoubanScraper
from app.schemas.types import MediaType
from app.utils.common import retry
from app.utils.system import SystemUtils


class DoubanModule(_ModuleBase):
    doubanapi: DoubanApi = None
    scraper: DoubanScraper = None

    def init_module(self) -> None:
        self.doubanapi = DoubanApi()
        self.scraper = DoubanScraper()

    def stop(self):
        pass

    def init_setting(self) -> Tuple[str, Union[str, bool]]:
        pass

    def douban_info(self, doubanid: str) -> Optional[dict]:
        """
        获取豆瓣信息
        :param doubanid: 豆瓣ID
        :return: 豆瓣信息
        """
        """
        {
          "rating": {
            "count": 287365,
            "max": 10,
            "star_count": 3.5,
            "value": 6.6
          },
          "lineticket_url": "",
          "controversy_reason": "",
          "pubdate": [
            "2021-10-29(中国大陆)"
          ],
          "last_episode_number": null,
          "interest_control_info": null,
          "pic": {
            "large": "https://img9.doubanio.com/view/photo/m_ratio_poster/public/p2707553644.webp",
            "normal": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2707553644.webp"
          },
          "vendor_count": 6,
          "body_bg_color": "f4f5f9",
          "is_tv": false,
          "head_info": null,
          "album_no_interact": false,
          "ticket_price_info": "",
          "webisode_count": 0,
          "year": "2021",
          "card_subtitle": "2021 / 英国 美国 / 动作 惊悚 冒险 / 凯瑞·福永 / 丹尼尔·克雷格 蕾雅·赛杜",
          "forum_info": null,
          "webisode": null,
          "id": "20276229",
          "gallery_topic_count": 0,
          "languages": [
            "英语",
            "法语",
            "意大利语",
            "俄语",
            "西班牙语"
          ],
          "genres": [
            "动作",
            "惊悚",
            "冒险"
          ],
          "review_count": 926,
          "title": "007：无暇赴死",
          "intro": "世界局势波诡云谲，再度出山的邦德（丹尼尔·克雷格 饰）面临有史以来空前的危机，传奇特工007的故事在本片中达到高潮。新老角色集结亮相，蕾雅·赛杜回归，二度饰演邦女郎玛德琳。系列最恐怖反派萨芬（拉米·马雷克 饰）重磅登场，毫不留情地展示了自己狠辣的一面，不仅揭开了玛德琳身上隐藏的秘密，还酝酿着危及数百万人性命的阴谋，幽灵党的身影也似乎再次浮出水面。半路杀出的新00号特工（拉什纳·林奇 饰）与神秘女子（安娜·德·阿玛斯 饰）看似与邦德同阵作战，但其真实目的依然成谜。关乎邦德生死的新仇旧怨接踵而至，暗潮汹涌之下他能否拯救世界？",
          "interest_cmt_earlier_tip_title": "发布于上映前",
          "has_linewatch": true,
          "ugc_tabs": [
            {
              "source": "reviews",
              "type": "review",
              "title": "影评"
            },
            {
              "source": "forum_topics",
              "type": "forum",
              "title": "讨论"
            }
          ],
          "forum_topic_count": 857,
          "ticket_promo_text": "",
          "webview_info": {},
          "is_released": true,
          "actors": [
            {
              "name": "丹尼尔·克雷格",
              "roles": [
                "演员",
                "制片人",
                "配音"
              ],
              "title": "丹尼尔·克雷格（同名）英国,英格兰,柴郡,切斯特影视演员",
              "url": "https://movie.douban.com/celebrity/1025175/",
              "user": null,
              "character": "饰 詹姆斯·邦德 James Bond 007",
              "uri": "douban://douban.com/celebrity/1025175?subject_id=27230907",
              "avatar": {
                "large": "https://qnmob3.doubanio.com/view/celebrity/raw/public/p42588.jpg?imageView2/2/q/80/w/600/h/3000/format/webp",
                "normal": "https://qnmob3.doubanio.com/view/celebrity/raw/public/p42588.jpg?imageView2/2/q/80/w/200/h/300/format/webp"
              },
              "sharing_url": "https://www.douban.com/doubanapp/dispatch?uri=/celebrity/1025175/",
              "type": "celebrity",
              "id": "1025175",
              "latin_name": "Daniel Craig"
            }
          ],
          "interest": null,
          "vendor_icons": [
            "https://img9.doubanio.com/f/frodo/fbc90f355fc45d5d2056e0d88c697f9414b56b44/pics/vendors/tencent.png",
            "https://img2.doubanio.com/f/frodo/8286b9b5240f35c7e59e1b1768cd2ccf0467cde5/pics/vendors/migu_video.png",
            "https://img9.doubanio.com/f/frodo/88a62f5e0cf9981c910e60f4421c3e66aac2c9bc/pics/vendors/bilibili.png"
          ],
          "episodes_count": 0,
          "color_scheme": {
            "is_dark": true,
            "primary_color_light": "868ca5",
            "_base_color": [
              0.6333333333333333,
              0.18867924528301885,
              0.20784313725490197
            ],
            "secondary_color": "f4f5f9",
            "_avg_color": [
              0.059523809523809625,
              0.09790209790209795,
              0.5607843137254902
            ],
            "primary_color_dark": "676c7f"
          },
          "type": "movie",
          "null_rating_reason": "",
          "linewatches": [
            {
              "url": "http://v.youku.com/v_show/id_XNTIwMzM2NDg5Mg==.html?tpa=dW5pb25faWQ9MzAwMDA4XzEwMDAwMl8wMl8wMQ&refer=esfhz_operation.xuka.xj_00003036_000000_FNZfau_19010900",
              "source": {
                "literal": "youku",
                "pic": "https://img1.doubanio.com/img/files/file-1432869267.png",
                "name": "优酷视频"
              },
              "source_uri": "youku://play?vid=XNTIwMzM2NDg5Mg==&source=douban&refer=esfhz_operation.xuka.xj_00003036_000000_FNZfau_19010900",
              "free": false
            },
          ],
          "info_url": "https://www.douban.com/doubanapp//h5/movie/20276229/desc",
          "tags": [],
          "durations": [
            "163分钟"
          ],
          "comment_count": 97204,
          "cover": {
            "description": "",
            "author": {
              "loc": {
                "id": "108288",
                "name": "北京",
                "uid": "beijing"
              },
              "kind": "user",
              "name": "雨落下",
              "reg_time": "2020-08-11 16:22:48",
              "url": "https://www.douban.com/people/221011676/",
              "uri": "douban://douban.com/user/221011676",
              "id": "221011676",
              "avatar_side_icon_type": 3,
              "avatar_side_icon_id": "234",
              "avatar": "https://img2.doubanio.com/icon/up221011676-2.jpg",
              "is_club": false,
              "type": "user",
              "avatar_side_icon": "https://img2.doubanio.com/view/files/raw/file-1683625971.png",
              "uid": "221011676"
            },
            "url": "https://movie.douban.com/photos/photo/2707553644/",
            "image": {
              "large": {
                "url": "https://img9.doubanio.com/view/photo/l/public/p2707553644.webp",
                "width": 1082,
                "height": 1600,
                "size": 0
              },
              "raw": null,
              "small": {
                "url": "https://img9.doubanio.com/view/photo/s/public/p2707553644.webp",
                "width": 405,
                "height": 600,
                "size": 0
              },
              "normal": {
                "url": "https://img9.doubanio.com/view/photo/m/public/p2707553644.webp",
                "width": 405,
                "height": 600,
                "size": 0
              },
              "is_animated": false
            },
            "uri": "douban://douban.com/photo/2707553644",
            "create_time": "2021-10-26 15:05:01",
            "position": 0,
            "owner_uri": "douban://douban.com/movie/20276229",
            "type": "photo",
            "id": "2707553644",
            "sharing_url": "https://www.douban.com/doubanapp/dispatch?uri=/photo/2707553644/"
          },
          "cover_url": "https://img9.doubanio.com/view/photo/m_ratio_poster/public/p2707553644.webp",
          "restrictive_icon_url": "",
          "header_bg_color": "676c7f",
          "is_douban_intro": false,
          "ticket_vendor_icons": [
            "https://img9.doubanio.com/view/dale-online/dale_ad/public/0589a62f2f2d7c2.jpg"
          ],
          "honor_infos": [],
          "sharing_url": "https://movie.douban.com/subject/20276229/",
          "subject_collections": [],
          "wechat_timeline_share": "screenshot",
          "countries": [
            "英国",
            "美国"
          ],
          "url": "https://movie.douban.com/subject/20276229/",
          "release_date": null,
          "original_title": "No Time to Die",
          "uri": "douban://douban.com/movie/20276229",
          "pre_playable_date": null,
          "episodes_info": "",
          "subtype": "movie",
          "directors": [
            {
              "name": "凯瑞·福永",
              "roles": [
                "导演",
                "制片人",
                "编剧",
                "摄影",
                "演员"
              ],
              "title": "凯瑞·福永（同名）美国,加利福尼亚州,奥克兰影视演员",
              "url": "https://movie.douban.com/celebrity/1009531/",
              "user": null,
              "character": "导演",
              "uri": "douban://douban.com/celebrity/1009531?subject_id=27215222",
              "avatar": {
                "large": "https://qnmob3.doubanio.com/view/celebrity/raw/public/p1392285899.57.jpg?imageView2/2/q/80/w/600/h/3000/format/webp",
                "normal": "https://qnmob3.doubanio.com/view/celebrity/raw/public/p1392285899.57.jpg?imageView2/2/q/80/w/200/h/300/format/webp"
              },
              "sharing_url": "https://www.douban.com/doubanapp/dispatch?uri=/celebrity/1009531/",
              "type": "celebrity",
              "id": "1009531",
              "latin_name": "Cary Fukunaga"
            }
          ],
          "is_show": false,
          "in_blacklist": false,
          "pre_release_desc": "",
          "video": null,
          "aka": [
            "007：生死有时(港)",
            "007：生死交战(台)",
            "007：间不容死",
            "邦德25",
            "007：没空去死(豆友译名)",
            "James Bond 25",
            "Never Dream of Dying",
            "Shatterhand"
          ],
          "is_restrictive": false,
          "trailer": {
            "sharing_url": "https://www.douban.com/doubanapp/dispatch?uri=/movie/20276229/trailer%3Ftrailer_id%3D282585%26trailer_type%3DA",
            "video_url": "https://vt1.doubanio.com/202310011325/3b1f5827e91dde7826dc20930380dfc2/view/movie/M/402820585.mp4",
            "title": "中国预告片：终极决战版 (中文字幕)",
            "uri": "douban://douban.com/movie/20276229/trailer?trailer_id=282585&trailer_type=A",
            "cover_url": "https://img1.doubanio.com/img/trailer/medium/2712944408.jpg",
            "term_num": 0,
            "n_comments": 21,
            "create_time": "2021-11-01",
            "subject_title": "007：无暇赴死",
            "file_size": 10520074,
            "runtime": "00:42",
            "type": "A",
            "id": "282585",
            "desc": ""
          },
          "interest_cmt_earlier_tip_desc": "该短评的发布时间早于公开上映时间，作者可能通过其他渠道提前观看，请谨慎参考。其评分将不计入总评分。"
        }
        """
        if not doubanid:
            return None
        logger.info(f"开始获取豆瓣信息：{doubanid} ...")
        douban_info = self.doubanapi.movie_detail(doubanid)
        if douban_info:
            celebrities = self.doubanapi.movie_celebrities(doubanid)
            if celebrities:
                douban_info["directors"] = celebrities.get("directors")
                douban_info["actors"] = celebrities.get("actors")
        else:
            douban_info = self.doubanapi.tv_detail(doubanid)
            celebrities = self.doubanapi.tv_celebrities(doubanid)
            if douban_info and celebrities:
                douban_info["directors"] = celebrities.get("directors")
                douban_info["actors"] = celebrities.get("actors")
        return douban_info

    def douban_discover(self, mtype: MediaType, sort: str, tags: str,
                        page: int = 1, count: int = 30) -> Optional[List[dict]]:
        """
        发现豆瓣电影、剧集
        :param mtype:  媒体类型
        :param sort:  排序方式
        :param tags:  标签
        :param page:  页码
        :param count:  数量
        :return: 媒体信息列表
        """
        logger.info(f"开始发现豆瓣 {mtype.value} ...")
        if mtype == MediaType.MOVIE:
            infos = self.doubanapi.movie_recommend(start=(page - 1) * count, count=count,
                                                   sort=sort, tags=tags)
        else:
            infos = self.doubanapi.tv_recommend(start=(page - 1) * count, count=count,
                                                sort=sort, tags=tags)
        if not infos:
            return []
        return infos.get("items") or []

    def movie_showing(self, page: int = 1, count: int = 30) -> List[dict]:
        """
        获取正在上映的电影
        """
        infos = self.doubanapi.movie_showing(start=(page - 1) * count,
                                             count=count)
        if not infos:
            return []
        return infos.get("subject_collection_items")

    def tv_weekly_chinese(self, page: int = 1, count: int = 30) -> List[dict]:
        """
        获取豆瓣本周口碑国产剧
        """
        infos = self.doubanapi.tv_chinese_best_weekly(start=(page - 1) * count,
                                                      count=count)
        if not infos:
            return []
        return infos.get("subject_collection_items")

    def tv_weekly_global(self, page: int = 1, count: int = 30) -> List[dict]:
        """
        获取豆瓣本周口碑外国剧
        """
        infos = self.doubanapi.tv_global_best_weekly(start=(page - 1) * count,
                                                     count=count)
        if not infos:
            return []
        return infos.get("subject_collection_items")

    def tv_animation(self, page: int = 1, count: int = 30) -> List[dict]:
        """
        获取豆瓣动画剧
        """
        infos = self.doubanapi.tv_animation(start=(page - 1) * count,
                                            count=count)
        if not infos:
            return []
        return infos.get("subject_collection_items")

    def search_medias(self, meta: MetaBase) -> Optional[List[MediaInfo]]:
        """
        搜索媒体信息
        :param meta:  识别的元数据
        :reutrn: 媒体信息
        """
        # 未启用豆瓣搜索时返回None
        if settings.SEARCH_SOURCE != "douban":
            return None

        if not meta.name:
            return []
        result = self.doubanapi.search(meta.name)
        if not result:
            return []
        # 返回数据
        ret_medias = []
        for item_obj in result.get("items"):
            if meta.type and meta.type.value != item_obj.get("type_name"):
                continue
            if item_obj.get("type_name") not in (MediaType.TV.value, MediaType.MOVIE.value):
                continue
            ret_medias.append(MediaInfo(douban_info=item_obj.get("target")))

        return ret_medias

    @retry(Exception, 5, 3, 3, logger=logger)
    def match_doubaninfo(self, name: str, mtype: str = None,
                         year: str = None, season: int = None) -> dict:
        """
        搜索和匹配豆瓣信息
        :param name:  名称
        :param mtype:  类型 电影/电视剧
        :param year:  年份
        :param season:  季号
        """
        result = self.doubanapi.search(f"{name} {year or ''}".strip(),
                                       ts=datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        if not result:
            logger.warn(f"未找到 {name} 的豆瓣信息")
            return {}
        # 触发rate limit
        if "search_access_rate_limit" in result.values():
            logger.warn(f"触发豆瓣API速率限制 错误信息 {result} ...")
            raise Exception("触发豆瓣API速率限制")
        for item_obj in result.get("items"):
            type_name = item_obj.get("type_name")
            if type_name not in [MediaType.TV.value, MediaType.MOVIE.value]:
                continue
            if mtype and mtype != type_name:
                continue
            if mtype == MediaType.TV and not season:
                season = 1
            item = item_obj.get("target")
            title = item.get("title")
            if not title:
                continue
            meta = MetaInfo(title)
            if type_name == MediaType.TV.value:
                meta.type = MediaType.TV
                meta.begin_season = meta.begin_season or 1
            if meta.name == name \
                    and ((not season and not meta.begin_season) or meta.begin_season == season) \
                    and (not year or item.get('year') == year):
                return item
        return {}

    def movie_top250(self, page: int = 1, count: int = 30) -> List[dict]:
        """
        获取豆瓣电影TOP250
        """
        infos = self.doubanapi.movie_top250(start=(page - 1) * count,
                                            count=count)
        if not infos:
            return []
        return infos.get("subject_collection_items")

    def scrape_metadata(self, path: Path, mediainfo: MediaInfo) -> None:
        """
        刮削元数据
        :param path: 媒体文件路径
        :param mediainfo:  识别的媒体信息
        :return: 成功或失败
        """
        if settings.SCRAP_SOURCE != "douban":
            return None
        if SystemUtils.is_bluray_dir(path):
            # 蓝光原盘
            logger.info(f"开始刮削蓝光原盘：{path} ...")
            meta = MetaInfo(path.stem)
            if not meta.name:
                return
            # 根据名称查询豆瓣数据
            doubaninfo = self.match_doubaninfo(name=mediainfo.title,
                                               mtype=mediainfo.type.value,
                                               year=mediainfo.year,
                                               season=meta.begin_season)
            if not doubaninfo:
                logger.warn(f"未找到 {mediainfo.title} 的豆瓣信息")
                return
            scrape_path = path / path.name
            self.scraper.gen_scraper_files(meta=meta,
                                           mediainfo=MediaInfo(douban_info=doubaninfo),
                                           file_path=scrape_path)
        else:
            # 目录下的所有文件
            for file in SystemUtils.list_files(path, settings.RMT_MEDIAEXT):
                if not file:
                    continue
                logger.info(f"开始刮削媒体库文件：{file} ...")
                try:
                    meta = MetaInfo(file.stem)
                    if not meta.name:
                        continue
                    # 根据名称查询豆瓣数据
                    doubaninfo = self.match_doubaninfo(name=mediainfo.title,
                                                       mtype=mediainfo.type.value,
                                                       year=mediainfo.year,
                                                       season=meta.begin_season)
                    if not doubaninfo:
                        logger.warn(f"未找到 {mediainfo.title} 的豆瓣信息")
                        break
                    # 刮削
                    self.scraper.gen_scraper_files(meta=meta,
                                                   mediainfo=MediaInfo(douban_info=doubaninfo),
                                                   file_path=file)
                except Exception as e:
                    logger.error(f"刮削文件 {file} 失败，原因：{e}")
        logger.info(f"{path} 刮削完成")
