import Data.List
import Data.Maybe

indexedSeries :: [Float] -> [(Int, Float)]
indexedSeries = zip [1 ..]

graphPairs :: [(Int, Float)] -> [[(Int, Float)]]
graphPairs g = concatMap (drop 2 . inits) $ init $ init $ tails g

-- graphPairs g = concatMap (drop 2 . inits) $ filter (\x -> length x >= 2) $ tails g
-- graphPairs g = concatMap (drop 2 . inits) $ dropLast 2 $ tails g

visiblePair :: [(Int, Float)] -> Maybe (Int, Int)
visiblePair list = if all isVisible (init . tail $ list) then Just (i, j) else Nothing
  where
    (i, x) = head list
    (j, y) = last list
    isVisible (k, z) = z < x + fromIntegral (k - i) / fromIntegral (j - i) * (y - x)

visibilityGraph :: [(Int, Float)] -> [(Int, Int)]
visibilityGraph s = map fromJust $ filter (/= Nothing) $ map visiblePair $ graphPairs s

horizontalPair :: [(Int, Float)] -> Maybe (Int, Int)
horizontalPair list = if all (\(_, z) -> z < m) (init . tail $ list) then Just (i, j) else Nothing
  where
    (i, x) = head list
    (j, y) = last list
    m = min x y

horizontalGraph :: [(Int, Float)] -> [(Int, Int)]
horizontalGraph s = map fromJust $ filter (/= Nothing) $ map horizontalPair $ graphPairs s

gramianAngularField :: [Double] -> [[Double]]
gramianAngularField s@(x : xs)
  | minS == maxS = []
  | otherwise = g
  where
    minS = minimum s
    maxS = maximum s
    f x = 2 * (x - minS) / (maxS - minS) - 1
    rescaled = map f s
    angles = map acos rescaled
    g = map (\x -> map (\y -> cos $ x + y) angles) angles
