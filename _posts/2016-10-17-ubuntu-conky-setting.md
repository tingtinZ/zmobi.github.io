---
layout: post
title: ubuntu conky设置
description: 设置conky方便监测工作机的系统情况，注意conky1.10与之前的版本有语法上的区别
category: Linux
keywords: ubuntu, conky, 点击桌面conky消失

---

前段时间重装了下工作机，发现没有`conky` 监测下系统信息好不自在，借着今天早上有空，把*conky* 装上，顺便整理下其设置，免得下次又花时间重复来折腾。

<!-- more -->

## conky安装

跑条命令即可，如果不同用户，建议新建个配置在家目录下，免得冲突。

```
sudo apt install conky
mkdir -pv ~/.config/conky
cp /etc/conky/conky.conf ~/.config/conky
```

## conky1.10配置

详细配置如下，其中部分有注释说明

```lua
conky.config = {  
    -- 设置conky对齐的位置，top_left为左上
    alignment = 'top_left',  
      
    background = false,  
      
    border_width = 1,  
      
    cpu_avg_samples = 2,  
    net_avg_samples = 2,  
      
    use_xft = true,  
    -- Xft font when Xft is enabled  
    font = 'Sans:size=11',  
    -- Text alpha when using Xft  
    xftalpha = 0.8,  
      
    default_color = 'white',  
    default_outline_color = 'green',  
    default_shade_color = 'green',  
      
    draw_borders = false,  
    draw_graph_borders = true,  
    draw_outline = false,  
    draw_shades = false,  
  
  	-- 设置水平 与 垂直 方面上，离屏幕边缘多少像素远
    gap_x = 100,  
    gap_y = 31,  
    minimum_height = 5,  
    minimum_width = 5,  
      
    no_buffers = true,  
    out_to_console = false,  
    out_to_stderr = false,  
    extra_newline = false,  
  	
  	-- double_buffer一定要选 true，否则连接的几项无效
    double_buffer = true,  
    -- Create own window instead of using desktop (required in nautilus)  
    own_window = true,  
    own_window_class = 'Conky',  
    -- 下两项为设置窗体透明度
    own_window_argb_visual = true,  
    own_window_transparent = true,  
    own_window_hints = 'undecorated,below,sticky,skip_taskbar,skip_pager', 
    -- 想要点击桌面时，conky内容不消失，必须设置为Normal
    own_window_type = 'normal',  
  
    stippled_borders = 0,  
    update_interval = 1.0,  
    uppercase = false,  
    use_spacer = 'none',  
    show_graph_scale = false,  
    show_graph_range = false  
}  

-- 下述内容，根据自身的网卡与硬盘信息做适应性whnt
conky.text = [[  
${color red}系统信息 ${hr 1}${color}  
主机名: $alignr$nodename  
内核版本: $alignr$kernel  
运行时长: $alignr$uptime  
  
CPU: ${alignr}${freq dyn} MHz  
进程数: ${alignr}$processes ($running_processes running)  
负载: ${alignr}$loadavg  
  
CPU ${alignr}${cpu cpu0}%  
${cpubar 4 cpu0}  
Ram ${alignr}$mem / $memmax ($memperc%)  
${membar 4}  
swap ${alignr}$swap / $swapmax ($swapperc%)  
${swapbar 4}  
  
CPU占用排行 $alignr CPU%  MEM%  
${top name 1}$alignr${top cpu 1}   ${top mem 1}  
${top name 2}$alignr${top cpu 2}   ${top mem 2}  
${top name 3}$alignr${top cpu 3}   ${top mem 3}  
  
内存占用排行 $alignr CPU%  MEM%  
${top_mem name 1}$alignr${top_mem cpu 1}   ${top_mem mem 1}  
${top_mem name 2}$alignr${top_mem cpu 2}   ${top_mem mem 2}  
${top_mem name 3}$alignr${top_mem cpu 3}   ${top_mem mem 3}  
  
${color green}网络信息 ${hr 1}${color}  
Down ${downspeed enp3s0}/s ${alignr}Up ${upspeed enp3s0}/s  
${downspeedgraph enp3s0 24,110} ${alignr}${upspeedgraph enp3s0 24,110}  
Total ${totaldown enp3s0} ${alignr}Total ${totalup enp3s0}  
  
${color pink}硬盘读写 ${hr 1}${color}  
Read ${diskio_read}/s ${alignr}Write ${diskio_write}/s  
${diskiograph_read /dev/sda 25,107} ${alignr}${diskiograph_read /dev/sda 25,107}  

${color yellow}硬盘空间 ${hr 1}${color}  
/home  $color${fs_used /home}/${fs_size /home}   ${fs_bar 5,120 /home}
/data  $color${fs_used /data}/${fs_size /data}   ${fs_bar 5,120 /data}   
/      $color${fs_used /}/${fs_size /}           ${fs_bar 5,120 /}
]] 
```

## 设置开机启动

```shell
cat > ~/.config/autostart/conky.desktop < EOF
[Desktop Entry]  
Type=Application  
Name=Conky  
Comment=Start conky script  
Exec=conky -d  
OnlyShowIn=GNOME  
X-GNOME-Autostart-Phase=Application  
Name[en_US]=conky.desktop  
EOF
```

> 参考：[conky 1.10设置](http://blog.csdn.net/little3344/article/details/47275647#)

