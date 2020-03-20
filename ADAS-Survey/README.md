# Advanced Driver Assistance Systems (ADAS) Survey Analysis -- October 2019

### What is this?

This repo contains work for a take-home assignment for a nonprofit publisher which performs research and investigative reporting in the service of consumers. This assignment was the first step in the interview process. I was not asked to continue to an actual interview after completing this assignment.

### What was this take-home about?

For this assignment, I was provided compiled survey data from **ADAS_Verbatim_Demo data for candidates.xlsx**, which details car owner satisfaction levels and free text feedback regarding their experiences with different ADAS types:

* Lane Departure Warning
* Front Collision Avoidance
* Rear Collision Avoidance
* Blind Spot Monitor
* Cruise Control

across a wide range of 2018 makes and models. Using this data, I was asked to create a written report or slide deck to report which systems drive better sentiment compared to others, focusing on:

* Features of systems driving positive/negative results
* Differences in experiences by model year, car make, or model that stood out

I have included the slide deck I created to describe my findings:

* [Keynote](ADASSurveyAnalysis.key)
* [PDF](ADASSurveyAnalysis.pdf)

The notebook [ADASSurveyAnalysis.ipynb]{ADASSurveyAnalysis.ipynb} provides the code used to create the slide decks for this assignment (Note: There was no requirement to submit this code). Perhaps eventually I will be including some additional code just to work on developing interactive visualizations.

### How long did you have to do this assignment?

~4 days. I was sent this assignment on a Friday and asked to submit what I had the following Tuesday (which I did).

### Notes

* I don't think I structured my slide deck particularly well in retrospect. Probably needed more slides to summarize findings up front and some of the more detailed slides describing findings for each particular system were a bit too busy and the key takeaways needed to be more salient.
* I felt I had good reason to reduce the satisfaction into basic Positive/Negative levels, but it may have simplified things too much? Also since I went down that road, it might have been stronger attempting something more rigorous (a supervised learning approach?) to capture which features drove specific sentiments.
* In revisiting this work, I noticed there were some responses that were either completely duplicated or duplicated aside from the reported car make/model. This was something I did not address properly for the assignment. If I were to have done that, for the completely duplicated rows (responses) If the, I would have just dropped one of the responses. Otherwise, for the nearly completely duplicated rows, I would have dropped all as it's difficult to untangle which of the multiple common responses is the correct one.
