/*
From:
https://community.alfresco.com/community/bpm/blog/2016/11/18/activiti-enterprise-developer-series-custom-rest-endpoints
*/

package com.activiti.extension.api;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;

@XmlRootElement(name = "greeting")
public class GreetingMessage implements Serializable {
    String name;
    String text;

    public GreetingMessage() {}

    public GreetingMessage(String name, String text) {
        this.name = name;
        this.text = text;
    }

    @XmlElement(name = "name")
    public String getName() {
        return name;
    }

    @XmlElement(name = "text")
    public String getText() {
        return text;
    }
}