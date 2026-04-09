Understanding and using this repo.

Managing Temp
-You will want to run your fans on full blast when using LLM as a judge or running a scoring run. 
-On mac you can control you fans this program with https://crystalidea.com/macs-fan-control. 
-On windows you might have to look around more- you can test this https://getfancontrol.com


Translating shorthand:
-anno means annotated with wireframes/pose estimation
-in the analysis files za means zero anno, wa means with anno

Use:
-the temp frame folder is deleted on demand by the scoring fucntions so you can feel free to handle it how you like
-The analysis files analyze socring run output of scoring runs
-utils.py has many handy functions with decenting- to extend this code you shoudld test and put more code in utils such the code in few shot crit.

Data:
-Videos are data, the ExtraVideos folder expands the initial toy data further allowing for deeper testing. 
