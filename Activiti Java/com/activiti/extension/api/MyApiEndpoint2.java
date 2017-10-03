/**
 * Copyright 2005-2017 Alfresco Software, Ltd. All rights reserved.
 * License rights for this program may be obtained from Alfresco Software, Ltd.
 * pursuant to a written agreement and any use of this program without such an
 * agreement is prohibited.
 */

/*
Authored by Grayson Cody Collins
Custom rest endpoint to execute custom sql query and map responses into Json
 */
package com.activiti.extension.api;
import com.codahale.metrics.annotation.Timed;
import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import io.swagger.annotations.ApiResponse;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyApiEndpoint2 {

    //sets to 'enterprise' mapping. names the custom endpoint as well as the method
    @Autowired
    @RequestMapping(value = "/enterprise/myRestEndpoint2",method = RequestMethod.GET,produces = "application/json")


    @Timed
    @ApiResponse(code =404, message = "You clearly did something wrong.")
    public static String main(String[] argv) {


    	//declare variables. RS is the results of the sql query. connection is the sql connection parameters,
        //jsonInString is the holder for Json response
    	ResultSet rs=null;
    	String jsonInString = null;
        Connection connection = null;
        ObjectMapper mapper = new ObjectMapper();

        //declare values of columns pulled from sql query to map into custom java object
        String apiTaskDefKey;
        String apiName;
        String apiType;
        String apiText;
        int apiProcInstId;

        List<RowObject> RowObjectList=new ArrayList<RowObject>();

        //initialize the custom java object, RowObject defined
        RowObject apiRowObject= new RowObject("", "", "", "", 0);

        

        System.out.println("222-------- Oracle JDBC Connection Testing ------");

        //looks for the JDBC driver jar which must be in the same class path as the rest jar.
        //tomcat/webapps/activiti-app/WEB-INF/lib
        try {

            Class.forName("oracle.jdbc.driver.OracleDriver");

        } catch (ClassNotFoundException e) {

            System.out.println("Where is your Oracle JDBC Driver?");
            e.printStackTrace();
            //return;

        }

        System.out.println("222Oracle JDBC Driver Registered!");



        //defines the connection parameters to the database. URL, username, and password
        try {

            connection = DriverManager.getConnection(
                    "jdbc:oracle:thin:@ec2-52-91-173-74.compute-1.amazonaws.com:1521:orcl", "OEMBENCHMARK", "Benchmark1");
            
            //if successful, execute the query defined below
            if (connection != null) {

                jsonInString ="";

                System.out.println("222Connection Successful");
                Statement stmt = connection.createStatement();

                String sql;
                sql = "select * from OEMBENCHMARK.aaaVar WHERE NAME_= 'label27' AND ROWNUM< 5";
                rs = stmt.executeQuery(sql);
                
                
                //use rs the resultset to map the column values returned by the query
                //each iteration of this loop equals one row returned
                while (rs.next()){
                	//String variable = rs.getString("TEXT_");
                	//System.out.println(variable);

                    apiTaskDefKey=rs.getString("TASK_DEF_KEY_");
                    apiName=rs.getString("NAME_");
                    apiType=rs.getString("TYPE_");
                    apiText=rs.getString("TEXT_");
                    apiProcInstId=rs.getInt("PROC_INST_ID_");

                    //System.out.println(apiTaskDefKey);
                    //System.out.println(apiName);
                    //System.out.println(apiType);
                    //System.out.println(apiText);
                    //System.out.println(apiProcInstId);


                    //map the results to the custom java object RowObject
                    apiRowObject = new RowObject(apiTaskDefKey, apiName, apiType, apiText, apiProcInstId);

                    RowObjectList.add(apiRowObject);



                }


                
            } else {
                System.out.println("Failed to make connection!");
            }

        } catch (SQLException e) {

            System.out.println("Connection Failed! Check output console");
            e.printStackTrace();
            //return;

        }

        if (connection == null) {
            System.out.println("Failed to make connection!");

            
        }



        //add results to jsonInString
        try {
            jsonInString =mapper.writerWithDefaultPrettyPrinter().writeValueAsString(RowObjectList);

        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }


        try{
        	connection.close();        
        }
        catch(SQLException e){
            System.out.println("WTF dude!");
        }

        System.out.println("jsonInString= "+jsonInString);
        return jsonInString;
    }
}