package com.example.pypongcontroller;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void onButton(View button) {
        if (button.getId()==R.id.button2)
            Toast.makeText(this, "UP", Toast.LENGTH_SHORT).show();
        if (button.getId()==R.id.button)
            Toast.makeText(this, "DOWN", Toast.LENGTH_SHORT).show();
    }
}
