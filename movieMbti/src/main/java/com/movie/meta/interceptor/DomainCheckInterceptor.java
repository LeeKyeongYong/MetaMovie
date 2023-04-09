package com.movie.meta.interceptor;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.Data;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.util.Arrays;
import java.util.List;
@Data
@Component
public class DomainCheckInterceptor implements HandlerInterceptor {

    private List<String> allowedDomains = Arrays.asList("movie/main.do", "/","/index.do");
    private String redirectUrl = "/";


    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String requestUrl = request.getRequestURL().toString();
        boolean allowed = allowedDomains.stream().anyMatch(requestUrl::contains);
        if (!allowed) {
            response.sendRedirect(redirectUrl);
            return false;
        }
        return true;
    }
}
