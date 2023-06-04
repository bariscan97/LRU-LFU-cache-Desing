## 460. LFU Cache


###

Design and implement a data structure for a [Least Frequently Used (LFU)](https://en.wikipedia.org/wiki/Least_frequently_used) cache.

Implement the `LFUCache` class:

-   `LFUCache(int capacity)` Initializes the object with the `capacity` of the data structure.
-   `int get(int key)` Gets the value of the `key` if the `key` exists in the cache. Otherwise, returns `-1`.
-   `void put(int key, int value)` Update the value of the `key` if present, or inserts the `key` if not already present. When the cache reaches its `capacity`, it should invalidate and remove the **least frequently used** `key` before inserting a new item. For this problem, when there is a **tie** (i.e., two or more keys with the same frequency), the **least recently used** `key` would be invalidated.

To determine the least frequently used key, a **use counter** is maintained for each key in the cache. The key with the smallest **use counter** is the least frequently used key.

When a key is first inserted into the cache, its use counter is set to `1` (due to the `put` operation). The **use counter** for a key in the cache is incremented either a `get` or `put` operation is called on it.

The functions `get` and `put` must each run in `O(1)` average time complexity.

#### Example 1:

```
Input
["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, 3, null, -1, 3, 4]

Explanation
// cnt(x) = the use counter for key x
// cache=[] will show the last used order for tiebreakers (leftmost element is  most recent)
LFUCache lfu = new LFUCache(2);
lfu.put(1, 1);   // cache=[1,_], cnt(1)=1
lfu.put(2, 2);   // cache=[2,1], cnt(2)=1, cnt(1)=1
lfu.get(1);      // return 1
                 // cache=[1,2], cnt(2)=1, cnt(1)=2
lfu.put(3, 3);   // 2 is the LFU key because cnt(2)=1 is the smallest, invalidate 2.
                 // cache=[3,1], cnt(3)=1, cnt(1)=2
lfu.get(2);      // return -1 (not found)
lfu.get(3);      // return 3
                 // cache=[3,1], cnt(3)=2, cnt(1)=2
lfu.put(4, 4);   // Both 1 and 3 have the same cnt, but 1 is LRU, invalidate 1.
                 // cache=[4,3], cnt(4)=1, cnt(3)=2
lfu.get(1);      // return -1 (not found)
lfu.get(3);      // return 3
                 // cache=[3,4], cnt(4)=1, cnt(3)=3
lfu.get(4);      // return 4
                 // cache=[3,4], cnt(4)=2, cnt(3)=3
```

#### Constraints:

-   `0 <= capacity <= 10`<sup>`4`</sup>
-   `0 <= key <= 10`<sup>`5`</sup>
-   `0 <= value <= 10`<sup>`9`</sup>
-   At most `2 * 10`<sup>`5`</sup> calls will be made to `get` and `put`.

#

-

```js
var LFUCache = function(capacity) {
  this.minCount = 0;
  this.keyValues = new Map();
  this.countKeys = new Map();
  this.capacity = capacity;
};

LFUCache.prototype.incrementCount = function(key, newValue = undefined) {
  
  let { value, count } = this.keyValues.get(key);
  if (newValue) value = newValue;
  this.keyValues.set(key, { value, count: count + 1 });
  
  const set = this.countKeys.get(count);
  set.delete(key);

  if (set.size === 0) {
    this.countKeys.delete(count);
    if (this.minCount === count) this.minCount += 1;
  } else {
    this.countKeys.set(count, set); 
  }

  this.countKeys.set(count + 1, (this.countKeys.get(count + 1) || new Set()).add(key));
  
  return value;
}

/** 
 * @param {number} key
 * @return {number}
 */
LFUCache.prototype.get = function(key) {
  if (!this.keyValues.has(key)) return -1;
  return this.incrementCount(key);
};

/** 
 * @param {number} key 
 * @param {number} value
 * @return {void}
 */
LFUCache.prototype.put = function(key, value) {
  if (this.capacity === 0) return;
  
  if (this.keyValues.has(key)) {
    this.incrementCount(key, value);
    return;
  }
    
  if (this.keyValues.size === this.capacity) {
    
    const set = this.countKeys.get(this.minCount);
    const keyToDelete = set.values().next().value;
    set.delete(keyToDelete);
    
    if (set.size === 0) {
      this.countKeys.delete(this.minCount);
    } else {
      this.countKeys.set(this.minCount, set); 
    }

    this.keyValues.delete(keyToDelete);
  }

  const count = 1;
  this.keyValues.set(key, { value, count });
  this.countKeys.set(count, (this.countKeys.get(count) || new Set()).add(key));
  this.minCount = count;  
};
-
/**
 * Your LFUCache object will be instantiated and called as such:
 * var obj = new LFUCache(capacity)
 * var param_1 = obj.get(key)
 * obj.put(key,value)
 */
```
