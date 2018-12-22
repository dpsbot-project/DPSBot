import os
import sys
import archiveis
import asyncio
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plugin.whisperandlog import bot_log
from trans_open import opentrans
_ = opentrans._
class archiveclass():
    def __init__(self, bot):
        self.bot = bot
        self.proxyString = "13.209.8.211:80"
        self.desired_capability = webdriver.DesiredCapabilities.FIREFOX
        self.desired_capability['proxy'] = {
            "proxyType": "manual",
            "httpProxy": self.proxyString,
            "sslProxy": self.proxyString
        }
        self.desired_capability["unexpectedAlertBehaviour"] = "accept"
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--log-level=3')
        self.options.add_argument('--mute-audio')
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("media.volume_scale", "0.0")
        self.profile.set_preference("intl.accept_languages", "ko")
        self.driver = webdriver.Firefox(self.profile, firefox_options=self.options, executable_path="/app/geckodriver")
        self.options.add_argument(
                {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'})


    @commands.command(name=_("아카이브"), pass_context=True)
    async def archive(self, ctx, url):
        await bot_log(_("%s가 %s를(을) 아카이브 했습니다.\n") % (ctx.message.author, url))
        try:
            if not "http" in url:
                url = "http://" + url
            archive_url = archiveis.capture(url, self.proxyString)
            await self.bot.send_message(ctx.message.channel, _("아카이브 중입니다...\n조금만 기다려 주세요!"))
            self.driver.get(url)
            wait = WebdriverWait(self.driver, 2)
            wait.until(EC.presence_of_element_located((By.XPATH, 'html')))
            self.driver.maximize_window()
            self.driver.find_element_by_tag_name('html').screenshot('screenshot.png')
            await self.bot.send_file(ctx.message.channel, 'screenshot.png')
            await self.bot.send_message(ctx.message.channel, archive_url)
            await self.bot.log(_("아카이브 주소:%s\n") % (url))
            os.remove('screenshot.png')
        except:
            try:
                self.driver.close()
            except:
                pass
            await self.bot.send_message(ctx.message.channel, _("오류가 발생했어요!"))
            raise


def setup(bot):
    bot.add_cog(archiveclass(bot))
