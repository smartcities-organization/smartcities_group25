(define (domain group25)
   (:predicates 
    (light ?l)
    (Heat ?h)
    (Cool ?c)
    (Temperature ?t)
    (isON ?on)
    (isOff ?off)
    (isGreater ?tc ?tt)
    (isLesser ?tc ?tt)
    (isEqual ?tc ?tt)
    (Hum_fr ?hr)
    (DeHum_fr ?dhr)
    (Humidity ?t)
    (inRange ?hc ?ht)
    )

(:action switchOn
       :parameters  (?led)
       :precondition (and  (light ?led) (isOff ?led) )
       :effect (and  (isON ?led)
         (not (isOff ?led))))
(:action switchOff
       :parameters  (?led)
       :precondition (and  (light ?led) (isON ?led) )
       :effect (and  (isOff ?led)
         (not (isON ?led))))
         
(:action HeaterOn
       :parameters  (?app1 ?app2 ?Tartem ?CurTem)
       :precondition (and  (Heat ?app1)(Cool ?app2)(Temperature ?Tartem) (Temperature ?CurTem )(isOff ?app1)(isOff ?app2)
                         (isLesser ?CurTem ?Tartem)(not(isEqual ?CurTem ?Tartem)))
       :effect (and  (isON ?app1)(not (isOff ?app1))(not (isLesser ?CurTem ?Tartem))(isEqual ?CurTem ?Tartem))
       )     
    
(:action HeaterOff
       :parameters  (?app1 ?Tartem ?CurTem)
       :precondition (and  (Heat ?app1)(Temperature ?Tartem) (Temperature ?CurTem )(isON ?app1)
                         (isGreater ?CurTem ?Tartem) (not(isEqual ?CurTem ?Tartem)))
       :effect (and  (isOff ?app1)(not (isON ?app1))(not (isGreater ?CurTem ?Tartem))(isEqual ?CurTem ?Tartem))
       )
       
(:action CoolerOn
       :parameters  (?app1 ?app2 ?Tartem ?CurTem)
       :precondition (and  (Heat ?app1)(Cool ?app2)(Temperature ?Tartem) (Temperature ?CurTem )(isOff ?app1)(isOff ?app2)
                         (isGreater ?CurTem ?Tartem) (not(isEqual ?CurTem ?Tartem)))
       :effect (and  (isON ?app2)(not (isOff ?app2))(not (isGreater ?CurTem ?Tartem))(isEqual ?CurTem ?Tartem))
       )     
    
(:action CoolerOff
       :parameters  (?app2 ?Tartem ?CurTem)
       :precondition (and  (Cool ?app2)(Temperature ?Tartem) (Temperature ?CurTem )(isON ?app2)
                         (isLesser ?CurTem ?Tartem) (not(isEqual ?CurTem ?Tartem)))
       :effect (and  (isOff ?app2)(not (isON ?app2))(not (isLesser ?CurTem ?Tartem))(isEqual ?CurTem ?Tartem))
       )
(:action ON_DeHumidifier
       :parameters  (?dhr ?TarHum ?CurHum)
       :precondition (and (Humidity ?TarHum) (Humidity ?CurHum )(isOFF ?dhr)(DeHum_fr ?dhr)
                         (isGreater ?CurHum ?TarHum)(not(inRange ?CurHum ?TarHum)))
       :effect (and  (isON ?dhr)(not (isOFF ?dhr))(not (isGreater ?CurHum ?TarHum))(inRange ?CurHum ?TarHum))
       )   
(:action ON_Humidifier
       :parameters  (?hr ?TarHum ?CurHum)
       :precondition (and  (Hum_fr ?hr)(Humidity ?TarHum) (Humidity ?CurHum )(isOFF ?hr)(Hum_fr ?hr)
                         (isLesser ?CurHum ?TarHum)(not(inRange ?CurHum ?TarHum)))
       :effect (and  (isON ?hr)(not (isOFF ?hr))(not (isLesser ?CurHum ?TarHum))(inRange ?CurHum ?TarHum))
       )
(:action OFF_Hum_DeHum
       :parameters  (?dhr ?hr ?TarHum ?CurHum)
       :precondition (and  (Hum_fr ?hr)(Humidity ?TarHum) (Humidity ?CurHum )(isON ?hr)(Hum_fr ?hr)(isON ?dhr)(DeHum_fr ?dhr)
                         (inRange ?CurHum ?TarHum))
       :effect (and  (isOFF ?hr)(isOFF ?dhr)))
   )

