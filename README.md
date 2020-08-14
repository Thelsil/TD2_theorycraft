***********************************************
#    THE DIVISION 2 - PVP THEORYCRAFTING TOOL  
***********************************************

This Python script implements a 1v1 face-trade simulator. It takes a lot of things into account, but of course it cannot 
exactly reproduce all the in-game complexity, and most of all, every situation. It is limited to 1v1 facetrade simulation 
without obstacles, no medkits, no way to run away. So, it is really close to the 1v1 DZ rules. If you want to theorycraft THE build for 1v1, this tool is perfect.
Now, have in mind that it can also be useful for regular PvP. Facetrade situations do happen a lot. 
Knowing how good your build manage these situations will get you an upper advantage over your opponents. 
You can also simulate situations where you or your enemy are flanked by simply delaying who is going to shoot first.


A tool is a tool. Depending on how you use it, it can be extremely useful or completely unadapted. 
Be creative! For instance, if your build is about flanking and beam as fast as possible, you may be interested about the 
time to kill your opponent before he has time to react. In such case, you can build a strong opponent that one shot you, 
and the probability of winning will translate into the probability of killing your opponent before he can react.

**DON'T** fully trust your own PvP experience! Everything is about probabilities. However, evolution has made us, 
human being, powerful correlation machines to improve our survivability. But that make us bad at understand probabilities. 
Have you heard of the Monty Hall problem? I suggest you to take a little of your time and read the related 
Wikipedia pages, this is a very unintuitive problem with an unintuitive solution, which demonstrate how bad we are at 
understanding probabilities. That's why we use math and simulations when dealing with probabilities. 
And that's also why I created this tool: if we want to improve in PvP, we **HAVE** to question our PvP experience 
with powerful heuristic and analytical tools. Mathematics and sciences are, in my opinion, 
the most overpowered things that human has invented. Why not use this power in video games too?

***********************************************
#    LIMATIONS OF THE TOOL  
***********************************************

Excepted the small shields, skills won't be supported, at least for now. This simulator only consider 
pure gun fights. Therefore, some approximation will be made for some talents that trigger on skills. 
Wicked, for instance, will be considered always activated. 

For now, specializations are barely supported. The Firewall will provide you +11% damages if you use a shield, and the 
Technician gives +1 shield skill tier. More feature targetting specialization will be considered soon.

There is currently no sanity check for the stats you input!! You can create builds that are impossible to make in practice. 
You need to be sure the parameters you enter are corrects! In the future, the interface may change and sanity check may be included.

Bonus armors are not implemented yet, so Intimidate + Adrenaline rush combo cannot be simulated. However, it is on top of
the priority for the implementation.
***********************************************
#    LIST OF SUPPORTED TALENTS 
***********************************************

__WEAPON TALENTS__

**In-Sync**: Always fully activated, giving 30% increased weapon damages.\
**Optimist**: Works as intended. Damages increase when the number of bullet in the magazine decrease.\
**Strained**: Works as intended. The longer you shoot, the higher your critical damages. Reset if you stop shooting (reloading).\
**Sadistic**: Always fully activated, giving 20% increased weapon damages.\
**Ignited**: Always fully activated, giving 20% increased weapon damages.\
**Eyeless**: Always fully activated, giving 20% increased weapon damages.\
<!--**Measured**: Works as intended.\
**Breadbasket**: Works as intended, with a slight approximation. For each bodyshot, a headshot damage stack is added, 
but last for the remaining of the fight instead of 10s to ease implementation. I mean, you must be really bad at aiming if you cannot
land any headshots during 10s... \
**Ranger**: Works as intended. The base shooting range is 15m, but it can be changed in faceTrade_simulator arguments (third input parameter).--->

NOTE: For Unhinged, just add +0.18 in the "IWD" attribute.

__CHESTPIECE TALENTS__

**Unbreakable**: Works as intended. Perfect version supported. When you armor break, regain 50% of your armor back. If you are damaged by high burst
damage and you lose all your health after your armor break, unbreakable won't proc and you are killed. Unbreakable cooldown is not taken into account as, 
generally,1v1 fights never last more than 45s. \
**Glasscanon**: Works as intended.\
**Spotter**: Always activated. Amplify weapon damages by 15%.\
**Spark**: Always activated. The duration (15s+) is very long given the current TTK, so it is assumed the talent last during the whole fight,
and you can easily re-activate it if required.
Increase total weapon damages by 15%.\
**Vanguard**: Works as intended. Considered activated at the start of the fight. Your shield cannot be damaged for 2s.\
**Obliterate**: Each time you score a critical hit, a total weapon damage stack is added to a buffer 
and last 5s. Note that stacks are not reseted/replaced when the buffer is full, I am not sure it's how it works in practice, but it can be easily corrected.


__BACKPACK TALENTS__
 
**Companion**: Considered always activated and provide +15% total weapon damages all the time.\
**Concussion**: The first buff works as intended. Increase total weapon damages for 1.5s (5 if MMR) if you headshot. 
The second buff, on kill condition, is however not supported.\
**Vigilance**: Works as intended. At the start of the fight, it is considered activated. If you get hit (not your shield), 
the buff is put into cooldown for 4s. The cooldown duration reset to 0 each time you are hit.
 
 