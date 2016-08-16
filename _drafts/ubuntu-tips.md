---
layout: post
title: Ubuntu小技巧收集
category: Linux
description: 用于收集ubuntu在日常使用过程中的一些小技巧，免除日后寻找麻烦，节省时间
---

### ssh-key 免除重复多次输入密码

在*.zshrc* 文件中，添加下列这行代码即可

```shell
sudo apt install keychain
# .zshrc 或者 .bashrc
eval `keychain --eval id_rsa`
```


### conky简单而快速的配置

```shell
conky.config = {  
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
    default_outline_color = 'white',  
    default_shade_color = 'white',  
      
    draw_borders = false,  
    draw_graph_borders = true,  
    draw_outline = false,  
    draw_shades = false,  
  
    gap_x = 75,  
    gap_y = 40,  
    minimum_height = 5,  
    minimum_width = 5,  
      
    no_buffers = true,  
    out_to_console = false,  
    out_to_stderr = false,  
    extra_newline = false,  
  
    double_buffer = true,  
    -- Create own window instead of using desktop (required in nautilus)  
    own_window = true,  
    own_window_class = 'Conky',  
    own_window_argb_visual = true,  
    own_window_transparent = true,  
    own_window_hints = 'undecorated,below,sticky,skip_taskbar,skip_pager',  
    own_window_type = 'desktop',  
  
    stippled_borders = 0,  
    update_interval = 1.0,  
    uppercase = false,  
    use_spacer = 'none',  
    show_graph_scale = false,  
    show_graph_range = false  
}  
  
conky.text = [[  
${color red}SYSTEM ${hr 1}${color}  
Hostname: $alignr$nodename  
Kernel: $alignr$kernel  
Uptime: $alignr$uptime  
  
CPU: ${alignr}${freq dyn} MHz  
Processes: ${alignr}$processes ($running_processes running)  
Load: ${alignr}$loadavg  
  
CPU ${alignr}${cpu cpu0}%  
${cpubar 4 cpu0}  
Ram ${alignr}$mem / $memmax ($memperc%)  
${membar 4}  
swap ${alignr}$swap / $swapmax ($swapperc%)  
${swapbar 4}  
  
Highest CPU $alignr CPU%  MEM%  
${top name 1}$alignr${top cpu 1}   ${top mem 1}  
${top name 2}$alignr${top cpu 2}   ${top mem 2}  
${top name 3}$alignr${top cpu 3}   ${top mem 3}  
  
Highest MEM $alignr CPU%  MEM%  
${top_mem name 1}$alignr${top_mem cpu 1}   ${top_mem mem 1}  
${top_mem name 2}$alignr${top_mem cpu 2}   ${top_mem mem 2}  
${top_mem name 3}$alignr${top_mem cpu 3}   ${top_mem mem 3}  
  
${color red}NETWORK ${hr 1}${color}  
Down ${downspeed enp3s0}/s ${alignr}Up ${upspeed enp3s0}/s  
${downspeedgraph enp3s0 25,107} ${alignr}${upspeedgraph enp3s0 25,107}  
Total ${totaldown enp3s0} ${alignr}Total ${totalup enp3s0}  
  
${color white}DISKIO ${hr 1}${color}  
Read ${diskio_read}/s ${alignr}Write ${diskio_write}/s  
${diskiograph_read /dev/sda 25,107} ${alignr}${diskiograph_read /dev/sda 25,107}  
]] 
```
