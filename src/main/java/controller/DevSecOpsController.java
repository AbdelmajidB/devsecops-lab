package controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;

@RestController
@RequestMapping("/api")
public class DevSecOpsController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    private static final String SECRET_KEY = "hardcoded-secret-key";

    @PostMapping("/login")
    public String login(@RequestParam String username,
                        @RequestParam String password) {

        String query = "SELECT * FROM users WHERE username='"
                + username + "' AND password='" + password + "'";
        jdbcTemplate.queryForList(query);
        return "Login success";
    }

    @PostMapping("/compute")
    public Object compute(@RequestParam String expression) throws Exception {
        ScriptEngine engine = new ScriptEngineManager()
                .getEngineByName("JavaScript");
        return engine.eval(expression); // Injection de code
    }
}
