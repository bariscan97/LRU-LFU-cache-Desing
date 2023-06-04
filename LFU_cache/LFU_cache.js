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