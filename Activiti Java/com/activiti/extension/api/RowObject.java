/**
 * Copyright 2005-2017 Alfresco Software, Ltd. All rights reserved.
 * License rights for this program may be obtained from Alfresco Software, Ltd.
 * pursuant to a written agreement and any use of this program without such an
 * agreement is prohibited.
 */

/*
Authored by Grayson Cody Collins
Java object to use for mapping in API response
 */

package com.activiti.extension.api;

public class RowObject {

    public RowObject(String taskDefKey, String name, String type, String text, int procInstId){
        this.taskDefKey = taskDefKey;
        this.name = name;
        this.type = type;
        this.text = text;
        this.procInstId=procInstId;
    }

    public RowObject() {
    }
	
	private String taskDefKey;
	private String name;
	private String type;
	private String text;
	private int procInstId;

	//getters
	public String getTaskDefKey(){
	    return taskDefKey;
    }

    public String getName(){
	    return name;
    }

    public String getType(){
        return type;
    }

    public String getText(){
        return text;
    }

    public int getProcInstId(){
        return procInstId;
    }

    //setters
    public void setTaskDefKey(String taskDefKey){
        this.procInstId=procInstId;
    }

    public void setName(String name){
        this.name=name;
    }

    public void setType(String type){
        this.type=type;
    }

    public void setText(String text){
        this.text=text;
    }

    public void setProcInstId (int procInstId){
        this.procInstId=procInstId;
    }

}
