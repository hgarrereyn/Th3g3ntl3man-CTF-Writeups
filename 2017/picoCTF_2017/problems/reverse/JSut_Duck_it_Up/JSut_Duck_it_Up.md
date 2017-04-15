# JSut Duck it Up
#### Writeup by hgarrereyn
* **Reverse Engineering**
* *75 points*
* Description: What in the world could this be?!?! file

# Links

**file**
```
placeholder
```

# Solution

At first glance, this file looks a little crazy. However, this problem is actually quite easy to solve. What we are looking at here is javascript type coercion taken to the max.

When you try to add two javascript objects of different types, the runtime engine will try to modify types in order to produce any result.

All we have to do to solve this problem is copy the file and paste it into the console of a browser where it will be converted into the following function (and immediately executed):

```js
(function() {
alert("aw_yiss_ducking_breadcrumbs_964eae3b")
})
```

Flag: `aw_yiss_ducking_breadcrumbs_964eae3b`

# Other

* [JSFuck](http://www.jsfuck.com/) provides a utility to create the same kind of obfuscated javascript as above.
