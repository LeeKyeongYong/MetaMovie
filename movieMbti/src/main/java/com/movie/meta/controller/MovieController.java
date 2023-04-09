package com.movie.meta.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class MovieController {

    @RequestMapping(value = {"/", "/index.do", "/main.do"} , method = {RequestMethod.GET, RequestMethod.POST})
    public String showMain(Model model) {
        return "/home/main";
    }
}
