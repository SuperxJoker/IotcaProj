package com.example.soilmoisturedisplay;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.Query;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {

    private TextView soilPercentageTextView;
    private DatabaseReference soilPercentageRef;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        soilPercentageTextView = findViewById(R.id.soilPercentageTextView);

        // Get a reference to the "Status" node in Firebase Realtime Database
        soilPercentageRef = FirebaseDatabase.getInstance().getReference().child("soil_percentage");

        // Retrieve the last recorded value from the database
        soilPercentageRef.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                Log.d("Snapshot info",   "ref: " + dataSnapshot.getRef().toString());
                Log.d("Snapshot info",   "value: " + dataSnapshot.getValue().toString());
                Log.d("Snapshot info",  "key: " +  dataSnapshot.getKey());

                if (dataSnapshot.exists()) {
                    String soilPercentage = dataSnapshot.getValue(String.class);
                    soilPercentageTextView.setText("Soil Percentage: " + soilPercentage + "%");
                } else {
                    soilPercentageTextView.setText("No data available");
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
                // Handle any errors that occur during data retrieval
                Log.d("Firebase", "Error retrieving soil percentage value: " + databaseError.getMessage());
            }
        });
    }
}

