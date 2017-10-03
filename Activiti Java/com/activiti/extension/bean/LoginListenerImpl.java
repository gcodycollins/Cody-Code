/**
 * Copyright 2005-2017 Alfresco Software, Ltd. All rights reserved.
 * License rights for this program may be obtained from Alfresco Software, Ltd.
 * pursuant to a written agreement and any use of this program without such an
 * agreement is prohibited.
 */

/*
Authored by Grayson Cody Collins
Custom function to do on successful login
 */

package com.activiti.extension.bean;

import com.activiti.api.security.LoginListener;
import com.activiti.domain.idm.User;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Component
public class LoginListenerImpl implements LoginListener {

    DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
    LocalDateTime now = LocalDateTime.now();

    @Override
    public void onLogin(User user) {

        System.out.println(dtf.format(now)+" User "+user.getEmail()+" has logged in@#@#");

    }
}