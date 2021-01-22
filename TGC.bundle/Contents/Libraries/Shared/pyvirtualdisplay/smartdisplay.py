import logging
import sys
import time

from PIL import Image, ImageChops

from pyvirtualdisplay import Display

if sys.platform == "darwin" or sys.platform == "win32":
    from PIL.ImageGrab import grab
else:
    from pyscreenshot import grab

log = logging.getLogger(__name__)


class DisplayTimeoutError(Exception):
    pass


class SmartDisplay(Display):
    def autocrop(self, im):
        """Crop borders off an image.

        :param im: Source image.
        :param bgcolor: Background color, using either a color tuple or a color name (1.1.4 only).
        :return: An image without borders, or None if there's no actual content in the image.
        """
        if im.mode != "RGB":
            im = im.convert("RGB")
        bg = Image.new("RGB", im.size, self._bgcolor)
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)
        return None  # no contents

    def grab(self, autocrop=True):
        img = grab()
        if sys.platform == "darwin" or sys.platform == "win32":
            img = grab(xdisplay=self.new_display_var)
        else:
            img = grab()

        if autocrop:
            img = self.autocrop(img)
        return img

    def waitgrab(self, timeout=60, autocrop=True, cb_imgcheck=None):
        """start process and create screenshot.
        Repeat screenshot until it is not empty and
        cb_imgcheck callback function returns True
        for current screenshot.

        :param autocrop: True -> crop screenshot
        :param timeout: int
        :param cb_imgcheck: None or callback for testing img,
                            True = accept img,
                            False = reject img
        """
        t = 0
        sleep_time = 0.3  # for fast windows
        repeat_time = 0.5
        while 1:
            log.debug("sleeping %s secs" % str(sleep_time))
            time.sleep(sleep_time)
            t += sleep_time
            img = self.grab(autocrop=autocrop)
            if img:
                if not cb_imgcheck:
                    break
                if cb_imgcheck(img):
                    break
            sleep_time = repeat_time
            repeat_time += 0.5  # progressive
            if t > timeout:
                msg = "Timeout! elapsed time:%s timeout:%s " % (t, timeout)
                raise DisplayTimeoutError(msg)
                # break

            log.debug("screenshot is empty, next try..")
        assert img
        #        if not img:
        #            log.debug('screenshot is empty!')
        return img
