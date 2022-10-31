## **[getPicrewInfos](https://github.com/ZWN2001/getPicrewInfos)**

### CN

参考https://github.com/Martinz64/picrew-archiver，仅供学习

`get_info.py`单线程爬取资源，测试过，一切正常

`get_info_async.py`使用了`aiohttp`，`aiofiles`，`asyncio`，会相对快，未测试，可能有bug。

#### 使用方法

获取你要爬取的捏脸id，形如：

```text
https://picrew.me/image_maker/id
```

修改变量id的值，`get_info.py`在第45行，`get_info_async.py`在第55行

`python3 get_info.py`或者像我一样用`pycharm`右键直接run就OK

其实你会发现原理十分简单

因为所有的图片资源链接都在网页里写的明明白白

&nbsp;

### EN

Reference：https://github.com/Martinz64/picrew-archiver

For study only.

`get_info.py` can download resource single-threaded, tested, everything is OK.

`get_info_async.py `  uses `aiohttp`，`aiofiles`，`asyncio`，maybe faster, but untested, maybe there are something wrong.

#### How to use it

Get the picrew id, like this:

```
https://picrew.me/image_maker/id
```

Change your id in `.py` file,  on the line 45 of `get_info.py`or on the line 55 of`get_info_async.py`. You can easily find it.

Then run `python3 get_info.py` or  right click and run with PyCharm just like me.
