(define (domain group25)
   (:predicates 
    (light ?l)
    (Appl ?a)
    (Temperature ?t)
    (isON ?on)
    (isOff ?off)
    (isGreater ?tc ?tt)
    (isLesser ?tc ?tt)
    (isEqual ?tc ?tt)
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
       :precondition (and  (Appl ?app1)(Appl ?app2)(Temperature ?Tartem) (Temperature ?CurTem )(isOff ?app1)(isOff ?app2)
                         (isLesser ?CurTem ?Tartem)(not(isEqual ?CurTem ?Tartem)))
       :effect (and  (isON ?app1)(not (isOff ?app1))(not (isLesser ?CurTem ?Tartem))(isEqual ?CurTem ?Tartem))
       )     
    
    (:action HeaterOff
       :parameters  (?app1 ?Tartem ?CurTem)
       :precondition (and  (Appl ?app1)(Temperature ?Tartem) (Temperature ?CurTem )(isON ?app1)
                         (isGreater ?CurTem ?Tartem) (not(isEqual ?CurTem ?Tartem)))
       :effect (and  (isOff ?app1)(not (isON ?app1))(not (isGreater ?CurTem ?Tartem))(isEqual ?CurTem ?Tartem))
       )
       
       (:action CoolerOn
       :parameters  (?app1 ?app2 ?Tartem ?CurTem)
       :precondition (and  (Appl ?app1)(Appl ?app2)(Temperature ?Tartem) (Temperature ?CurTem )(isOff ?app1)(isOff ?app2)
                         (isGreater ?CurTem ?Tartem) (not(isEqual ?CurTem ?Tartem)))
       :effect (and  (isON ?app2)(not (isOff ?app2))(not (isGreater ?CurTem ?Tartem))(isEqual ?CurTem ?Tartem))
       )     
    
    (:action CoolerOff
       :parameters  (?app2 ?Tartem ?CurTem)
       :precondition (and  (Appl ?app2)(Temperature ?Tartem) (Temperature ?CurTem )(isON ?app2)
                         (isLesser ?CurTem ?Tartem) (not(isEqual ?CurTem ?Tartem)))
       :effect (and  (isOff ?app2)(not (isON ?app2))(not (isLesser ?CurTem ?Tartem))(isEqual ?CurTem ?Tartem))
       )
         
   )

