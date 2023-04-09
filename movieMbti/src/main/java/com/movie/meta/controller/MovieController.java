package com.movie.meta.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class MovieController {

    @RequestMapping(value = "movie/main.do", method = {RequestMethod.GET, RequestMethod.POST})
    public String index(Model model) {

        return "/home/main";
    }

    @RequestMapping(value = {"/", "/index.do"} , method = {RequestMethod.GET, RequestMethod.POST})
    public String showMain(Model model) {

        return "/home/index";
    }
}
