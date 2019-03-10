function GetNewShows() {
   
  var shows = new java.util.ArrayList();
   

  var defaults = new Array;
  defaults.title_default = '$title';
  defaults.line1_default = '$episode';
  defaults.line2_default = '$release';
  defaults.line3_default = '';//'$rating - $runtime';
  defaults.line4_default = '';//'$number - $studio';
  defaults.icon = 'none';
  shows.add(defaults);
    
 

   var files =  MediaFileAPI.GetMediaFiles("T");
   files = Database.Sort(files,true,"GetAiringStartTime");
   var s = files.length;
   if (s > 3)
	s = 3;

   var reply = '';

  
for (var i=s-1;i>-1;i--) {
      var mf = files[i];

airing = MediaFileAPI.GetMediaFileAiring(mf);
airdate = AiringAPI.GetAiringStartTime(airing);
d = new Date('Jan 1, 1970 GMT');
d.setUTCMilliseconds(airdate);
airdate = d.toISOString();   

reply = airdate;

title = AiringAPI.GetAiringTitle(airing);
reply += ' ' + title;


episodeName = MediaFileAPI.GetMediaFileMetadata(mf,'EpisodeName');
reply += ' ' + episodeName ;

mediaID = MediaFileAPI.GetMediaFileID(mf);
//posterURL = 'http://192.168.1.4:8080/sagex/media/poster/'+mediaID;

posterURL = 'http://192.168.1.4:8080/sagex/media/fanart?artifact=poster&scalex=200&mediafile=' +mediaID;


fanartURL = 'http://192.168.1.4:8080/sagex/media/banner/' +mediaID;

season = MediaFileAPI.GetMediaFileMetadata(mf,'SeasonNumber');
episode = MediaFileAPI.GetMediaFileMetadata(mf,'EpisodeNumber');

reply += ' ' + posterURL;

var temp = new Array;
temp.title = title;
temp.airdate = airdate;
temp.episode = episodeName;
temp.poster = posterURL;
temp.number = 'S'+season+'E'+episode;
temp.flag = 'false'
temp.release = 'Recorded: $day, $time';
temp.rating = 7.4;
temp.runtime = 30;
shows.add(temp);


   }

var airings = Global.GetScheduledRecordings();  
var s = airings.length;
if (s == 0)
  return shows;

   if (s > 1)
	s = 2;

   var reply = '';

  
for (var i=0;i<s;i++) {
      var airing = airings[i];

airdate = AiringAPI.GetAiringStartTime(airing);
d = new Date('Jan 1, 1970 GMT');
d.setUTCMilliseconds(airdate);
airdate = d.toISOString();   


title = AiringAPI.GetAiringTitle(airing);

show = AiringAPI.GetShow(airing);


episodeName = ShowAPI.GetShowEpisode(show);
season = ShowAPI.GetShowSeasonNumber(show);
episode = ShowAPI.GetShowEpisodeNumber(show);

posterURL = 'http://192.168.1.4:8080/sagex/media/fanart?artifact=poster&scalex=200&mediatype=tv&title=' +title ;


fanartURL = 'http://192.168.1.4:8080/sagex/media/banner/' +mediaID;



reply += ' ' + posterURL;

var temp = new Array;
temp.title = title;
temp.airdate = airdate;
temp.episode = episodeName;
temp.poster = posterURL;
temp.number = 'S'+season+'E'+episode;
temp.flag = 'false'
temp.release = 'Upcomming: $day, $time';
temp.rating = 7.4;
temp.runtime = 30;
shows.add(temp);


   }
   return shows;

}
function GetCurrentShow(extender) {

var defaults = new Array;
defaults.poster = "";
defaults.title = "";
defaults.duration = 0;
defaults.watchedDuration= 0;
defaults.isPlaying = "False";

var UIContext =  Packages.sagex.UIContext;

var mf;
var watchedDuration;
if (extender == 0){
var names = Global.GetConnectedClients();
if (names.length == 0)
 return defaults;
mf = MediaPlayerAPI.GetCurrentMediaFile(new UIContext(names[0]));
watchedDuration = MediaPlayerAPI.GetRawMediaTime(new UIContext(names[0]))/1000;
}else{
mf = MediaPlayerAPI.GetCurrentMediaFile(new UIContext(extender));
watchedDuration = MediaPlayerAPI.GetRawMediaTime(new UIContext(extender))/1000;
}

airing = MediaFileAPI.GetMediaFileAiring(mf);

mediaID = MediaFileAPI.GetMediaFileID(mf);


posterURL = 'http://192.168.1.4:8080/sagex/media/fanart?artifact=poster&scalex=200&mediafile=' +mediaID;

airing = MediaFileAPI.GetMediaFileAiring(mf);
title = AiringAPI.GetAiringTitle(airing);

duration = MediaFileAPI.GetFileDuration(mf)/1000;

var names = Global.GetConnectedClients();



if(mediaID !=0){
defaults.poster = posterURL;
defaults.title = title;
defaults.isPlaying = "True";
defaults.duration = duration;
defaults.watchedDuration= watchedDuration;
}
return defaults;

  }
function Command(cmd,extender) {

var UIContext =  Packages.sagex.UIContext;
if (extender == 0){
var names = Global.GetConnectedClients();
Global.SageCommand(new UIContext(names[0]),cmd);
}else
Global.SageCommand(new UIContext(extender),cmd);

}

function PlayPause(extender) {

var UIContext =  Packages.sagex.UIContext;
if (extender == 0){
var names = Global.GetConnectedClients();
MediaPlayerAPI.PlayPause(new UIContext(names[0]));
}else
MediaPlayerAPI.PlayPause(new UIContext(extender));
}

function Seek(extender, time) {


var UIContext =  Packages.sagex.UIContext;



if (extender == 0){
var names = Global.GetConnectedClients();
mf = MediaPlayerAPI.GetCurrentMediaFile(new UIContext(names[0]));
minTime = MediaFileAPI.GetFileStartTime(mf);

MediaPlayerAPI.Seek(new UIContext(names[0]),minTime + time*1000);
}else{
mf = MediaPlayerAPI.GetCurrentMediaFile(new UIContext(extender));
minTime = MediaFileAPI.GetFileStartTime(mf);
MediaPlayerAPI.Seek(new UIContext(extender),minTime + time*1000);
}

}


