import Data.List.Extra

stuff = map make [
  (13, 11),
  (5, 0),
  (17, 11),
  (3, 0),
  (7, 2),
  (19, 17)
  ]
stuff_b = stuff ++ [make (11, 0)]
stuff' = map make [
  (5, 4),
  (2, 1)
  ]

make (cnt, start) = drop start $ cycle (True : replicate (cnt-1) False)

step = map tail

ready state = all (\i -> (state' !! i) !! i) [0..length state-1]
  where state' = step state

search i state =
  if ready state then i else
    search (i+1) (step state)

-- when actually doing it I just poked at things in ghci though
main = putStrLn $ show $ (search 0 stuff, search 0 stuff_b)
