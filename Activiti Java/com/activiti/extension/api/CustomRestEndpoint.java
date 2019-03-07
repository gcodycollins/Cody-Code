package com.activiti.extension.api;

import com.activiti.extension.api.GreetingMessage;
import com.codahale.metrics.annotation.Timed;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/enterprise")
public class CustomRestEndpoint {

    @RequestMapping(value = "/CustomRestEndpoint", method= RequestMethod.GET)
    public GreetingMessage sayHello(@RequestParam(value="name", required=false,
            defaultValue="World") String name) {
        GreetingMessage msg = new GreetingMessage(name, "Hello " + name + "!");
        return msg;
    }

    @RequestMapping(value = "/CustomRestEndpoint/{name}", method= RequestMethod.GET)
    public GreetingMessage sayHelloAgain(@PathVariable String name) {
        GreetingMessage msg = new GreetingMessage(name, "Hello " + name + "!");
        return msg;
    }

    @Timed
    public static void main(String[] argv) {

        System.out.println("---------------------------------------------------");
        System.out.println("---------------------------------------------------");
        System.out.println("-------- Custom Endpoint Successfully called ------");
        System.out.println("---------------------------------------------------");
        System.out.println("---------------------------------------------------");

    }

}
