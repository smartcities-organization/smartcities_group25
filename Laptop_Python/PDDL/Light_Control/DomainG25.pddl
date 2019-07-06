(define (domain group25)
   (:predicates 
    (light ?l)
    (isON ?on)
    (isOff ?off))

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
   )

