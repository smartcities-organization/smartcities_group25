﻿(define (problem HVAC)
   (:domain group25)
   (:objects Heater Cooler TargetT CurrentT)
   (:init (Heat Heater)
          (Cool Cooler)
          (Temperature TargetT)
          (Temperature CurrentT)
          (isLesser CurrentT TargetT)
          (isOff Heater)
          (isOff Cooler)
          )
   (:goal (and(isON Heater)
              (isOff Cooler)
              )))