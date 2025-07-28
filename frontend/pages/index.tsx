import type { NextPage } from "next";
import { VStack, Heading, HStack, Text, Box } from "@chakra-ui/react";
import { Card } from "../components/Card";
import { CreateUserVital } from "../components/CreateUserVital";
import { useState } from "react";
import useSWR from "swr";
import { fetcher } from "../lib/client";
import { ChatInterface } from "../components/ChatInterface";
const Home: NextPage = () => {
  const [userID, setUserID] = useState(null);
  const { data } = useSWR("/users/", fetcher);

  const usersFiltered = data?.users ? data.users : [];

  return (
    <VStack
      my={10}
      px={10}
      backgroundColor={"#fcfdff"}
      height={"100vh"}
      spacing={10}
      alignItems={"flex-start"}
    >
      <Heading size={"lg"} fontWeight={800}>
        RevDoc AI Engineering Interview
      </Heading>
      <VStack width={"100%"} alignItems={"flex-start"}>
        <Box width={"100%"}>
          <CreateUserVital
            users={usersFiltered}
            onCreate={setUserID}
            onSelect={setUserID}
          />
        </Box>
        <Box width={"100%"}>
          <ChatInterface userId={userID} />
        </Box>
      </VStack>
    </VStack>
  );
};

export default Home;
