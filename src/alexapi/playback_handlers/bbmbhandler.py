import threading
import logging
import vlc
from .vlchandler import VlcHandler, PlaybackAudioType


logger = logging.getLogger(__name__)


class BbmbHandler(VlcHandler):
    def sup():
        pass

    def on_play(self, item):
        logger.info("item url is " + item.url)

        # process audio

        # fork
            # animate mouth

        return super (BbmbHandler, self).on_play(item)
