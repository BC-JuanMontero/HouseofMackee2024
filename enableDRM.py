#!/usr/bin/env python3
from mackee import main, GetCMS

#===========================================
# callback to enable DRM
#===========================================
def enableDRM(video):
	# does video have DRM?
	if(video.get('drm_disabled') == True):
		# get the video ID
		videoID = str(video.get('id'))
		# create the JSON body
		jsonBody = ('{ "drm_disabled": false }')
		# make the PATCH call
		r = GetCMS().UpdateVideo(videoID=videoID, jsonBody=jsonBody)
		# check if all went well
		if(r.status_code in [200,202]):
			print(('Enabled DRM for video ID {videoid} with status {status}.').format(videoid=videoID, status=r.status_code))
		# otherwise report the error
		else:
			print(('Error code {error} enabling DRM for video ID {videoid}:').format(error=r.status_code, videoid=videoID))
			print(r.text)

#===========================================
# only run code if it's not imported
#===========================================
if __name__ == '__main__':
	main(enableDRM)
