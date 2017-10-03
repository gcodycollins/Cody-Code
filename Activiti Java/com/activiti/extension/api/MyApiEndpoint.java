/**
 * Copyright 2005-2017 Alfresco Software, Ltd. All rights reserved.
 * License rights for this program may be obtained from Alfresco Software, Ltd.
 * pursuant to a written agreement and any use of this program without such an
 * agreement is prohibited.
 */
package com.activiti.extension.api;

import com.codahale.metrics.annotation.Timed;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyApiEndpoint {
	
    @Autowired
    @RequestMapping(value = "/enterprise/myRestEndpoint",method = RequestMethod.GET,produces = "application/json")

    @Timed
    public static void main(String[] argv) {

        System.out.println("-------- Oracle JDBC Connection Testing ------");

        try {

            Class.forName("oracle.jdbc.driver.OracleDriver");

        } catch (ClassNotFoundException e) {

            System.out.println("Where is your Oracle JDBC Driver?");
            e.printStackTrace();
            return;

        }

        System.out.println("Oracle JDBC Driver Registered!");

        Connection connection = null;

        try {

            connection = DriverManager.getConnection(
                    "jdbc:oracle:thin:@ec2-52-91-173-74.compute-1.amazonaws.com:1521:orcl", "OEMBENCHMARK", "Benchmark1");
            
            
            if (connection != null) {
                System.out.println("Connection Successful");
                Statement stmt = connection.createStatement();
                ResultSet rs;
                rs = stmt.executeQuery("select * from OEMBENCHMARK.aaaVar WHERE NAME_= 'label27' AND ROWNUM= 1");
                
                while (rs.next()){
                	String variable = rs.getString("TEXT_");
                	System.out.println(variable);
                }
                
                connection.close();
                
            } else {
                System.out.println("Failed to make connection!");
            }

        } catch (SQLException e) {

            System.out.println("Connection Failed! Check output console");
            e.printStackTrace();
            return;

        }

        if (connection == null) {
            System.out.println("Failed to make connection!");

            
        }
    }

}