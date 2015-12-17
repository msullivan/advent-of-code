-- XXX: why did I write code for this instead of just modifying the input file?

import Data.List
import Data.Word
import Data.Maybe
import Data.Bits
import qualified Data.Char
import qualified Data.Map as Map

type Signals = Map.Map String Word16

lookupSignal :: Signals -> String -> Word16
lookupSignal signals key = Map.findWithDefault (read key) key signals

computeGate :: [String] -> Signals -> Word16
computeGate cmd signals = comp cmd
  where comp [x, "AND", y] = val x .&. val y
        comp [x, "OR",  y] = val x .|. val y
        comp [x, "LSHIFT",  y] = val x `shiftL` (fromEnum $ val y)
        comp [x, "RSHIFT",  y] = val x `shiftR` (fromEnum $ val y)
        comp ["NOT",  x] = complement $ val x
        comp [x] = val x

        val = lookupSignal signals

processGate :: Signals -> String -> (String, Word16)
processGate signals cmd =
  let (gate, ["->", output]) = break (== "->") $ words cmd
  in (output, computeGate gate signals)

makeSignals :: [String] -> [(String, Word16)] -> Signals
makeSignals cmds start = signals
  -- Feed the signals back into the computation lazily
  where signals = Map.fromList $ map (processGate signals) cmds ++ start

lol cmds =
  let compute_a start = fromJust $ Map.lookup "a" $ makeSignals cmds start
      a_val = compute_a []
  in compute_a [("b", a_val)]

answer f = interact $ (++"\n") . show . f
main = answer $ lol . lines
