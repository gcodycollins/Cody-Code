/**
 * Copyright 2005-2017 Alfresco Software, Ltd. All rights reserved.
 * License rights for this program may be obtained from Alfresco Software, Ltd.
 * pursuant to a written agreement and any use of this program without such an
 * agreement is prohibited.
 */

/*
Authored by Grayson Cody Collins
custom fucntion to do on log out
 */

package com.activiti.extension.bean;

import com.activiti.api.security.LogoutListener;
import com.activiti.domain.idm.User;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Component
public class LogoutListenerImpl implements LogoutListener {

    DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
    LocalDateTime now = LocalDateTime.now();

    @Override
    public void onLogout(User user) {



        System.out.println(dtf.format(now)+" User "+user.getEmail()+" has logged out@#@#");

    }
}